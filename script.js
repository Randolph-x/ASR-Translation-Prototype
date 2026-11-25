const el = id => document.getElementById(id);
let current = null;
let activeExample = null;
let flagged = false;
let busy = false;

async function request(path, example) {
  const response = await fetch(`/api/${path}?example=${encodeURIComponent(example)}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Simulation failed');
  return data;
}
function setBusy(value) {
  busy = value;
  for (const id of ['start', 'scenario', 'correct', 'originalBtn', 'flag']) {
    el(id).disabled = value;
  }
}
function updateReview() {
  const reviewing = current.needs_review || flagged;
  el('correctionBox').hidden = !reviewing || !current.correction;
  // Manual review must be available even when the simulated score is high.
  el('flag').hidden = current.needs_review || flagged || !current.correction;
  el('warning').hidden = !reviewing;
  el('warning').textContent = current.needs_review
    ? '⚠ Low confidence. Verify the original English before trusting this translation.'
    : '⚠ You flagged this caption. A high confidence score does not guarantee accuracy.';
}
function render(data, corrected = false) {
  current = data;
  flagged = false;
  el('result').hidden = false;
  el('translated').textContent = data.translation;
  el('original').textContent = data.original;
  el('suggestion').textContent = data.correction;
  el('score').textContent = `Confidence: ${data.confidence}%`;
  el('score').className = data.needs_review ? 'low' : '';
  el('originalBox').hidden = true;
  el('originalBtn').setAttribute('aria-expanded', 'false');
  el('originalBtn').textContent = 'View original English';
  updateReview();
  el('notice').textContent = corrected
    ? 'Suggested correction confirmed. 95% is a simulated post-review indicator.'
    : data.needs_review ? 'Please compare the original before confirming.'
    : 'You can continue following the lecture. Confidence is not proof of accuracy.';
}
el('scenario').addEventListener('change', () => {
  current = null;
  activeExample = null;
  flagged = false;
  el('result').hidden = true;
  el('slide').hidden = true;
  el('status').textContent = 'Ready to listen';
});
el('start').addEventListener('click', async () => {
  if (busy) return;
  const example = el('scenario').value;
  setBusy(true);
  current = null;
  activeExample = null;
  el('result').hidden = true;
  el('slide').hidden = true;
  el('status').textContent = 'Processing simulated lecturer speech…';
  try {
    const data = await request('simulate', example);
    activeExample = example;
    el('slide').hidden = example !== 'fifteen_high';
    render(data);
    el('status').textContent = 'Translation ready';
  } catch (error) {
    el('status').textContent = `Could not load caption: ${error.message}`;
  } finally { setBusy(false); }
});
el('originalBtn').addEventListener('click', () => {
  if (!current || busy) return;
  const show = el('originalBox').hidden;
  el('originalBox').hidden = !show;
  el('originalBtn').setAttribute('aria-expanded', String(show));
  el('originalBtn').textContent = show ? 'Hide original English' : 'View original English';
});
el('flag').addEventListener('click', () => {
  if (!current || busy || !current.correction) return;
  flagged = true;
  updateReview();
  el('notice').textContent = 'Caption flagged. Compare the original before confirming a correction.';
});
el('correct').addEventListener('click', async () => {
  if (!current || busy || !current.correction || !(current.needs_review || flagged)) return;
  if (el('originalBox').hidden) {
    el('notice').textContent = 'View the original English before confirming a correction.';
    return;
  }
  setBusy(true);
  try { render(await request('correct', activeExample), true); }
  catch (error) { el('notice').textContent = `Correction failed: ${error.message}`; }
  finally { setBusy(false); }
});
