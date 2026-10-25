from pathlib import Path
import json
import shutil
import hashlib
from PIL import Image, ImageDraw

r = Path("docs/architecture/spikes/real-video-ocr")
(r / "frames").mkdir(exist_ok=True)
(r / "crops").mkdir(exist_ok=True)
base = Path("vb-workspace/notes/media/x7X9w_GIm1s")
for t in [30, 40, 60, 70, 80, 90, 100, 120]:
    if not (r / "frames" / f"python-{t}.jpg").exists():
        shutil.copy2(
            base / f"frame_{t * 1000:08d}.jpg", r / "frames" / f"python-{t}.jpg"
        )
assert (r / "frames/diagram-820985.jpg").exists(), (
    "Use the committed captured diagram frame"
)
rows = []


def add(frame, split, box, text, kind="code"):
    n = len(rows) + 1
    name = f"{n:02d}"
    im = Image.open(r / "frames" / frame)
    im.crop(box).save(r / "crops" / f"{name}.png")
    rows.append(
        dict(
            id=name,
            frame="frames/" + frame,
            path=f"crops/{name}.png",
            split=split,
            box=box,
            expected=text,
            kind=kind,
        )
    )


for frame, box, text in [
    ("python-30.jpg", [210, 480, 705, 602], "WEB APPS"),
    ("python-30.jpg", [960, 576, 1225, 678], "django"),
    ("python-40.jpg", [88, 50, 330, 110], "TERMINAL"),
    ("python-40.jpg", [84, 182, 579, 259], ">>> import this"),
    ("python-60.jpg", [65, 40, 260, 90], "EXPLORER"),
    ("python-60.jpg", [205, 214, 306, 275], "hello"),
    ("python-60.jpg", [65, 1018, 255, 1066], "OUTLINE"),
    ("python-70.jpg", [185, 320, 717, 388], "hello = 'hi mom'"),
    ("python-80.jpg", [185, 215, 900, 287], "my_tuple = ('a', 'b')"),
    ("python-80.jpg", [185, 380, 760, 447], "my_list = [1,2,3]"),
]:
    add(
        frame,
        "tune",
        box,
        text,
        "code" if " = " in text or text.startswith(">>>") else "ui_label",
    )
for box, text in [
    ([775, 300, 1055, 362], "if True:"),
    ([909, 382, 1345, 444], "if condition:"),
    ([1040, 464, 1484, 529], 'print("true")'),
    ([908, 546, 1084, 610], "else:"),
    ([1040, 629, 1520, 692], 'print("false")'),
]:
    add("python-90.jpg", "heldout", box, text)
for box, text in [
    ([185, 290, 693, 352], "def have_fun():"),
    ([320, 373, 928, 437], "for i in range(5):"),
    ([460, 452, 731, 518], "print(i)"),
]:
    add("python-100.jpg", "heldout", box, text)
for box, text in [
    ([187, 215, 662, 275], "class Reptile:"),
    ([255, 295, 1153, 359], "def __init__(self, length):"),
    ([321, 378, 1031, 442], "self.length = length"),
    ([187, 542, 895, 605], "class Snake(Reptile):"),
    ([320, 624, 930, 687], "def slither(self):"),
]:
    add("python-120.jpg", "heldout", box, text)
for box, text, kind in [
    ([512, 65, 1408, 154], "AUDIO SYNTHESIS PLAN", "diagram_label"),
    ([176, 269, 594, 329], "AUDIO SOURCES", "diagram_label"),
    ([211, 598, 637, 660], "AUDIO WORKLET", "diagram_label"),
    ([175, 678, 665, 724], "Plays combinations of sines.", "diagram_text"),
    ([175, 724, 635, 771], "Runs in a separate thread.", "diagram_text"),
    ([835, 266, 1110, 291], "var audioContext:AudioContext;", "small_code"),
    ([835, 290, 1074, 314], "var node:AudioWorkletNode;", "small_code"),
]:
    add("diagram-820985.jpg", "heldout", box, text, kind)
(r / "cases.json").write_text(json.dumps(rows, indent=2) + "\n")
hashes = {
    str(p.relative_to(r)): hashlib.sha256(p.read_bytes()).hexdigest()
    for p in sorted(r.rglob("*"))
    if p.is_file() and (p.parent.name in ["frames", "crops"] or p.name == "cases.json")
}
(r / "frozen-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
c = Image.new("RGB", (1400, 120 * ((len(rows) + 1) // 2)), "#444")
d = ImageDraw.Draw(c)
for i, row in enumerate(rows):
    im = Image.open(r / row["path"])
    im.thumbnail((690, 80))
    x = i % 2 * 700
    y = i // 2 * 120
    c.paste(im, (x, y + 28))
    d.text((x + 3, y + 4), row["id"] + " " + row["split"], fill="white")
c.save(r / "label-contact.jpg")
print(
    "frozen", len(rows), "cases", sum(x["split"] == "heldout" for x in rows), "heldout"
)
