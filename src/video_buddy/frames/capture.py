from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess

from ..fetch.yt_dlp_opts import apply_youtube_auth

FRAME_NAME_PATTERN = re.compile(r"^frame_(\d+)\.jpg$")
VIDEO_SUFFIXES = {".mp4", ".mkv", ".mov", ".webm", ".m4v"}


def format_duration(seconds: int | float | None) -> str:
    if not seconds:
        return "0:00"
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def video_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def download_video(
    url: str,
    output_dir: Path,
    *,
    timeout: int = 600,
    cookies_from_browser: str | None = None,
) -> Path:
    import yt_dlp

    output_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "bv*[vcodec^=avc]+ba/bv*[vcodec^=hev]+ba/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "outtmpl": str(output_dir / "%(id)s.%(ext)s"),
        "socket_timeout": timeout,
    }
    apply_youtube_auth(ydl_opts, cookies_from_browser)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            candidates = []
            for item in info.get("requested_downloads") or []:
                filepath = item.get("filepath")
                if filepath:
                    candidates.append(Path(filepath))
            filename = info.get("_filename")
            if filename:
                candidates.append(Path(filename))
            prepared = Path(ydl.prepare_filename(info))
            candidates.append(prepared)
            if prepared.suffix.lower() != ".mp4":
                candidates.append(prepared.with_suffix(".mp4"))

        for candidate in candidates:
            if candidate.exists() and candidate.suffix.lower() in VIDEO_SUFFIXES:
                return candidate

        video_id = info.get("id")
        if video_id:
            for match in sorted(output_dir.glob(f"{video_id}.*")):
                if match.suffix.lower() in VIDEO_SUFFIXES:
                    return match
    except Exception as error:
        raise RuntimeError(f"Failed to download video: {error}") from error

    raise RuntimeError("Failed to locate downloaded video file")


def detect_scenes(
    video_path: Path,
    *,
    scene_detection_max_duration_s: int = 600,
) -> list[tuple[float, float]]:
    try:
        from scenedetect import SceneManager, open_video
        from scenedetect.detectors import ContentDetector
    except ImportError:
        return [(0.0, _video_duration_seconds(video_path))]

    video = open_video(str(video_path))
    duration = video.duration.get_seconds() if video.duration is not None else 0.0
    if duration <= 0:
        raise RuntimeError(f"Could not determine duration for {video_path}")
    if duration > scene_detection_max_duration_s:
        return [(0.0, duration)]

    try:
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector())
        scene_manager.detect_scenes(video)
        scenes = [
            (start.get_seconds(), end.get_seconds())
            for start, end in scene_manager.get_scene_list()
            if end.get_seconds() > start.get_seconds()
        ]
        return scenes or [(0.0, duration)]
    except Exception:
        return [(0.0, duration)]


def extract_frames(
    video_path: Path,
    scenes: list[tuple[float, float]],
    output_dir: Path,
    *,
    fps: float = 2.0,
    max_candidates: int = 200,
    ffmpeg_bin: str | None = None,
) -> list[Path]:
    if fps <= 0:
        raise ValueError("fps must be greater than 0")
    total_duration = sum(end - start for start, end in scenes)
    if total_duration <= 0:
        return []

    effective_fps = fps
    if len(scenes) <= 2 and total_duration > 300:
        effective_fps = min(fps, max_candidates / total_duration)
        effective_fps = max(1 / 60.0, effective_fps)

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = output_dir / "_raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    extracted_frames: list[Path] = []

    for index, (start_time, end_time) in enumerate(scenes):
        duration = max(0.0, end_time - start_time)
        if duration <= 0:
            continue
        pattern = raw_dir / f"scene_{index:04d}_%05d.jpg"
        _run_ffmpeg(
            [
                _ffmpeg_bin(ffmpeg_bin),
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{start_time:.3f}",
                "-t",
                f"{duration:.3f}",
                "-i",
                str(video_path),
                "-vf",
                f"fps={round(effective_fps, 4)}",
                "-q:v",
                "2",
                "-y",
                str(pattern),
            ]
        )
        raw_frames = sorted(raw_dir.glob(f"scene_{index:04d}_*.jpg"))
        if not raw_frames:
            midpoint = start_time + duration / 2
            timestamp_ms = int(round(midpoint * 1000))
            output_path = output_dir / f"frame_{timestamp_ms:08d}.jpg"
            extracted_frames.append(
                _extract_single_frame(
                    video_path, midpoint, output_path, ffmpeg_bin=ffmpeg_bin
                )
            )
            continue

        for frame_index, raw_frame in enumerate(raw_frames):
            timestamp = min(
                end_time, start_time + ((frame_index + 0.5) / effective_fps)
            )
            timestamp_ms = int(round(timestamp * 1000))
            output_path = output_dir / f"frame_{timestamp_ms:08d}.jpg"
            if output_path.exists():
                raw_frame.unlink(missing_ok=True)
                continue
            raw_frame.replace(output_path)
            extracted_frames.append(output_path)
        if len(extracted_frames) >= max_candidates:
            break

    shutil.rmtree(raw_dir, ignore_errors=True)
    extracted_frames.sort()
    return extracted_frames


def score_frame(frame_path: Path) -> dict[str, float | bool | str]:
    import cv2
    import imagehash
    from PIL import Image

    image = cv2.imread(str(frame_path))
    if image is None:
        raise RuntimeError(f"Failed to load frame: {frame_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = float(edges.astype(bool).sum() / edges.size * 100.0)
    brightness = float(gray.mean())
    face_area_ratio = 0.0

    with Image.open(frame_path) as pil_image:
        frame_hash = str(imagehash.phash(pil_image))

    should_ocr = 30.0 <= brightness <= 240.0
    should_include = edge_density >= 2.0 and 20.0 <= brightness <= 245.0
    return {
        "edge_density": round(edge_density, 3),
        "face_area_ratio": round(face_area_ratio, 4),
        "brightness": round(brightness, 3),
        "hash": frame_hash,
        "should_ocr": should_ocr,
        "should_include": should_include,
    }


def select_frames(
    frame_paths: list[Path], *, video_id: str, max_frames: int = 15
) -> list[dict]:
    if max_frames <= 0:
        raise ValueError("max_frames must be greater than 0")
    candidates = []
    for frame_path in sorted(frame_paths):
        score = score_frame(frame_path)
        timestamp_ms = parse_timestamp_ms(frame_path)
        candidates.append(
            {
                "video_id": video_id,
                "path": str(frame_path),
                "filename": frame_path.name,
                "timestamp_ms": timestamp_ms,
                "timestamp": format_timestamp_human(timestamp_ms),
                "timestamp_human": format_timestamp_human(timestamp_ms),
                "score": round(selection_score(score), 3),
                "edge_density": score["edge_density"],
                "face_area_ratio": score["face_area_ratio"],
                "brightness": score["brightness"],
                "hash": score["hash"],
                "should_ocr": score["should_ocr"],
                "should_include": score["should_include"],
            }
        )
    candidates.sort(
        key=lambda item: (
            bool(item["should_include"]),
            bool(item["should_ocr"]),
            float(item["score"]),
            -int(item["timestamp_ms"]),
        ),
        reverse=True,
    )

    selected: list[dict] = []
    selected_hashes: list[str] = []
    min_ts = min((candidate["timestamp_ms"] for candidate in candidates), default=0)
    max_ts = max((candidate["timestamp_ms"] for candidate in candidates), default=0)
    duration_ms = max_ts - min_ts
    bucket_width_ms = max(1, duration_ms // max_frames) if candidates else 1
    max_per_bucket = max(1, max_frames // 4)
    bucket_counts: dict[int, int] = {}

    for candidate in candidates:
        if len(selected) >= max_frames:
            break
        if any(
            hash_distance(str(candidate["hash"]), existing) <= 6
            for existing in selected_hashes
        ):
            continue
        idx = (candidate["timestamp_ms"] - min_ts) // bucket_width_ms
        if bucket_counts.get(idx, 0) >= max_per_bucket:
            continue
        if not candidate["should_include"] and len(selected) < max_frames // 2:
            continue
        selected.append(candidate)
        selected_hashes.append(str(candidate["hash"]))
        bucket_counts[idx] = bucket_counts.get(idx, 0) + 1

    selected.sort(key=lambda item: int(item["timestamp_ms"]))
    return selected


def capture_video_frames(
    video_id: str,
    *,
    media_dir: Path,
    max_frames: int = 15,
    cookies_from_browser: str | None = None,
    timeout: int = 600,
    ffmpeg_bin: str | None = None,
    scene_detection_max_duration_s: int = 600,
) -> dict:
    media_dir.mkdir(parents=True, exist_ok=True)
    download_dir = media_dir / "_download"
    raw_frames_dir = media_dir / "_frames_tmp"
    video_path = download_video(
        video_url(video_id),
        download_dir,
        timeout=timeout,
        cookies_from_browser=cookies_from_browser,
    )
    try:
        scenes = detect_scenes(
            video_path,
            scene_detection_max_duration_s=scene_detection_max_duration_s,
        )
        extracted = extract_frames(
            video_path,
            scenes,
            raw_frames_dir,
            ffmpeg_bin=ffmpeg_bin,
        )
        selected = select_frames(extracted, video_id=video_id, max_frames=max_frames)
        for frame in selected:
            source_path = Path(str(frame["path"]))
            destination_path = media_dir / source_path.name
            if source_path != destination_path:
                shutil.copy2(source_path, destination_path)
            frame["path"] = str(destination_path)
        return {
            "video_id": video_id,
            "total_extracted": len(extracted),
            "total_selected": len(selected),
            "frames": [
                {
                    "video_id": video_id,
                    "filename": frame["filename"],
                    "timestamp_ms": frame["timestamp_ms"],
                    "timestamp_human": frame["timestamp_human"],
                    "edge_density": frame["edge_density"],
                    "face_area_ratio": frame["face_area_ratio"],
                    "brightness": frame["brightness"],
                    "hash": frame["hash"],
                    "should_ocr": frame["should_ocr"],
                    "should_include": frame["should_include"],
                }
                for frame in selected
            ],
        }
    finally:
        shutil.rmtree(download_dir, ignore_errors=True)
        shutil.rmtree(raw_frames_dir, ignore_errors=True)


def write_frames_metadata(path: Path, metadata: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def parse_timestamp_ms(frame_path: Path) -> int:
    match = FRAME_NAME_PATTERN.match(frame_path.name)
    if not match:
        raise ValueError(f"Invalid frame filename: {frame_path.name}")
    return int(match.group(1))


def format_timestamp_human(timestamp_ms: int) -> str:
    return format_duration(timestamp_ms // 1000)


def selection_score(frame_score: dict[str, float | bool | str]) -> float:
    edge_density = float(frame_score["edge_density"])
    brightness = float(frame_score["brightness"])
    score = edge_density * 3.0
    brightness_bonus = max(0.0, 100.0 - abs(brightness - 120.0)) / 100.0 * 20.0
    score += brightness_bonus
    if bool(frame_score["should_ocr"]):
        score += 20.0
    if bool(frame_score["should_include"]):
        score += 10.0
    return score


def hash_distance(left: str, right: str) -> int:
    import imagehash

    return imagehash.hex_to_hash(left) - imagehash.hex_to_hash(right)


def _extract_single_frame(
    video_path: Path,
    timestamp: float,
    output_path: Path,
    *,
    ffmpeg_bin: str | None = None,
) -> Path:
    _run_ffmpeg(
        [
            _ffmpeg_bin(ffmpeg_bin),
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            f"{timestamp:.3f}",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            "-y",
            str(output_path),
        ]
    )
    if not output_path.exists():
        raise RuntimeError(f"ffmpeg did not produce frame: {output_path.name}")
    return output_path


def _run_ffmpeg(command: list[str]) -> None:
    subprocess.run(command, check=True, capture_output=True, text=True)


def _ffmpeg_bin(value: str | None = None) -> str:
    return value or shutil.which("ffmpeg") or "ffmpeg"


def _video_duration_seconds(video_path: Path) -> float:
    command = [_ffmpeg_bin(), "-i", str(video_path), "-f", "null", "-"]
    result = subprocess.run(command, capture_output=True, text=True)
    match = re.search(r"Duration: (\d+):(\d+):(\d+)\.(\d+)", result.stderr)
    if not match:
        return 0.0
    hours, minutes, seconds, centis = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds + centis / 100
