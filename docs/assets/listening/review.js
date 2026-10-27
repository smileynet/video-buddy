/* Personal listening review: private browser state; no uploads or model execution. */
(() => {
  const root = document.getElementById('blind-listening');
  if (!root) return;
  const $ = id => document.getElementById('blind-' + id);
  const assetSet = 'sha256:1af1229527c282d03867f1e7da048f3103b82f25d441f8bd3983e0a3cca1cfaa';
  const storageKey = 'video-buddy.personal-listening.v1';
  const names = ['Qwen3-TTS 0.6B Base', 'Chatterbox-Turbo'];
  const clips = {outcome: ['clip01.flac', 'clip02.flac'], mechanism: ['clip03.flac', 'clip04.flac']};
  const scripts = {
    outcome: 'Make a short narration, replace one paragraph, and keep its captions aligned. You are done when the revised audio plays in order, the unchanged takes are retained, and the captions match what you hear.',
    mechanism: 'Each paragraph is a replaceable audio unit. Arrange accepted units in script order, then derive caption and visual timing from the final narration. A longer replacement can shift the timing of everything after it.'
  };
  const emptyDraft = () => ({ratings: {A: {}, B: {}}, preference: '', notes: '', plays: {A: 0, B: 0, reference: 0}});
  const fresh = () => {
    const bit = crypto.getRandomValues(new Uint8Array(1))[0] % 2;
    return {id: new Date().toISOString(), order: bit ? [1, 0] : [0, 1], revealed: false,
      drafts: {outcome: emptyDraft(), mechanism: emptyDraft()}};
  };
  let state = {version: 1, current: fresh(), records: []};
  let persistent = true;
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey));
    if (saved && saved.version === 1 && saved.current && Array.isArray(saved.records)) state = saved;
  } catch (_) { persistent = false; }
  let pair = 'outcome';
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); }
    catch (_) { persistent = false; }
    $('privacy').textContent = persistent
      ? 'Drafts and saved preferences stay in this browser. Download a review to keep or share a copy; nothing is sent automatically.'
      : 'This browser cannot save the review across reloads. Download your review before leaving; nothing is sent automatically.';
  }
  const draft = () => state.current.drafts[pair];
  function collect() {
    for (const side of ['A', 'B']) for (const criterion of ['clarity', 'naturalness', 'likeness']) {
      draft().ratings[side][criterion] = $(criterion + '-' + side).value;
    }
    draft().preference = $('preference').value;
    draft().notes = $('notes').value;
    save();
  }
  function render() {
    for (const side of ['A', 'B']) {
      const player = $('audio-' + side);
      player.pause();
      player.src = 'assets/listening/' + clips[pair][state.current.order[side === 'A' ? 0 : 1]];
      for (const criterion of ['clarity', 'naturalness', 'likeness']) $(criterion + '-' + side).value = draft().ratings[side][criterion] || '';
    }
    $('script').textContent = scripts[pair];
    $('preference').value = draft().preference;
    $('notes').value = draft().notes;
    const recorded = state.records.some(r => r.review_id === state.current.id && r.paragraph === pair);
    $('reveal').disabled = !recorded || state.current.revealed;
    $('download').disabled = state.records.length === 0;
    $('export').disabled = state.records.length === 0;
    $('identities').hidden = !state.current.revealed;
    $('identities').textContent = state.current.revealed
      ? 'A: ' + names[state.current.order[0]] + ' · B: ' + names[state.current.order[1]] + '. Further ratings in this review are made with model identities known.' : '';
    $('count').textContent = state.records.length + ' saved preference' + (state.records.length === 1 ? '' : 's') + ' in this browser.';
    $('receipt').hidden = true;
    save();
  }
  for (const side of ['A', 'B']) for (const criterion of ['clarity', 'naturalness', 'likeness']) {
    const select = $(criterion + '-' + side);
    for (const [value, label] of [['', 'Choose…'], ['1', '1 · Low'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5 · High'], ['unsure', 'Not sure']]) {
      select.add(new Option(label, value));
    }
    select.addEventListener('change', collect);
  }
  $('notes').addEventListener('input', collect);
  $('preference').addEventListener('change', collect);
  $('paragraph').addEventListener('change', () => { collect(); pair = $('paragraph').value; render(); $('status').textContent = 'Same A/B assignment, new paragraph. Rate this paragraph separately.'; });
  for (const side of ['A', 'B', 'reference']) {
    const player = $('audio-' + side);
    const label = side === 'reference' ? 'reference' : side;
    $('play-' + side).addEventListener('click', async () => {
      if (!player.paused) { player.pause(); return; }
      try { await player.play(); }
      catch (_) { $('status').textContent = 'Playback could not start. Try the audio controls or reopen this dashboard in your browser.'; }
    });
    player.addEventListener('pause', () => { $('play-' + side).textContent = 'Play ' + label; });
    player.addEventListener('ended', () => { $('play-' + side).textContent = 'Play ' + label; });
    $('audio-' + side).addEventListener('play', () => {
      $('play-' + side).textContent = 'Pause ' + label;
      for (const other of ['A', 'B', 'reference']) if (other !== side) $('audio-' + other).pause();
      draft().plays[side]++; save();
    });
  }
  $('record').addEventListener('click', () => {
    collect();
    const complete = ['A', 'B'].every(side => ['clarity', 'naturalness', 'likeness'].every(c => draft().ratings[side][c]));
    if (!complete || !draft().preference) {
      $('status').textContent = 'Choose a rating (or Not sure) for each quality and select your preference. Nothing has been recorded as a completed review yet.';
      return;
    }
    state.records.push({review_id: state.current.id, saved_at: new Date().toISOString(), paragraph: pair,
      asset_set: assetSet, audio_files: {A: clips[pair][state.current.order[0]], B: clips[pair][state.current.order[1]], reference: 'reference.flac'},
      ratings: JSON.parse(JSON.stringify(draft().ratings)), preference: draft().preference, notes: draft().notes,
      play_events: {...draft().plays}, labels_hidden_when_saved: !state.current.revealed,
      ...(state.current.revealed ? {models: {A: names[state.current.order[0]], B: names[state.current.order[1]]}} : {})});
    render(); $('status').textContent = persistent ? 'Preference saved in this browser. Reveal the models when you are ready.' : 'Preference recorded in this open page. Download it before leaving.';
  });
  $('reveal').addEventListener('click', () => {
    if (!state.records.some(r => r.review_id === state.current.id && r.paragraph === pair)) return;
    state.current.revealed = true;
    for (const record of state.records) if (record.review_id === state.current.id) record.models = {A: names[state.current.order[0]], B: names[state.current.order[1]]};
    render(); $('status').textContent = 'Models revealed. Your original ratings remain recorded with their blind-label status.';
  });
  const exportData = () => ({format: 'video-buddy.personal-listening.v1', assets: 'assets/listening/manifest.json', asset_set: assetSet,
    level_matching: 'Constant gain to common RMS; original durations unchanged',
    scope: 'Personal self-reported preference; prior exposure uncontrolled; not an independent blinded study or objective quality score', records: state.records});
  $('export').addEventListener('click', () => { $('receipt').hidden = false; $('receipt').value = JSON.stringify(exportData(), null, 2); $('receipt').focus(); $('receipt').select(); });
  $('download').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([JSON.stringify(exportData(), null, 2)], {type: 'application/json'}));
    const link = document.createElement('a'); link.href = url; link.download = 'video-buddy-listening-review.json'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  $('new').addEventListener('click', () => {
    collect(); state.current = fresh(); render();
    $('status').textContent = 'New randomized assignment. Previous saved preferences are retained. Familiarity with the voices may still influence your ratings.';
  });
  render();
})();
