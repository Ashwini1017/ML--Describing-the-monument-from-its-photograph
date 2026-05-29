/**
 * app.js — Monument Vision Frontend Logic
 * Handles: drag-drop upload, prediction API calls,
 *          result rendering, history, model comparison
 */

// ── State ──────────────────────────────────────────────────
let currentFile = null;
let currentResult = null;

// ── DOM References ─────────────────────────────────────────
const imageInput    = document.getElementById('imageInput');
const dropZone      = document.getElementById('dropZone');
const previewSection = document.getElementById('previewSection');
const previewImg    = document.getElementById('previewImg');
const loadingCard   = document.getElementById('loadingCard');
const resultCard    = document.getElementById('resultCard');
const compareCard   = document.getElementById('compareCard');
const errorCard     = document.getElementById('errorCard');

// ── Init ───────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  checkModelStatus();
  setupDragDrop();
  imageInput.addEventListener('change', handleFileSelect);
});

// ── Model Status Check ─────────────────────────────────────
async function checkModelStatus() {
  const badge    = document.getElementById('modelStatusBadge');
  const dotText  = badge.querySelector('.status-text');
  try {
    const res  = await fetch('/models_status');
    const data = await res.json();
    badge.className = 'status-badge ' + (data.trained ? 'status-ready' : 'status-error');
    dotText.textContent = data.trained ? 'Models Ready' : 'Not Trained';
  } catch {
    badge.className = 'status-badge status-error';
    dotText.textContent = 'Server Offline';
  }
}

// ── Drag & Drop ────────────────────────────────────────────
function setupDragDrop() {
  dropZone.addEventListener('dragover', e => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      processFile(file);
    } else {
      showToast('Please drop an image file.', 'error');
    }
  });
}

function handleFileSelect(e) {
  const file = e.target.files[0];
  if (file) processFile(file);
}

function processFile(file) {
  currentFile = file;
  const reader = new FileReader();
  reader.onload = e => {
    previewImg.src = e.target.result;
    dropZone.classList.add('hidden');
    document.getElementById('sampleGallery').classList.add('hidden');
    previewSection.classList.remove('hidden');
    hideAll();
  };
  reader.readAsDataURL(file);
}

// ── Reset ──────────────────────────────────────────────────
function resetUpload() {
  currentFile   = null;
  currentResult = null;
  imageInput.value = '';
  previewImg.src   = '';
  previewSection.classList.add('hidden');
  dropZone.classList.remove('hidden');
  document.getElementById('sampleGallery').classList.remove('hidden');
  hideAll();
}

// ── Load Sample Image ──────────────────────────────────────
async function loadSampleImage(url) {
  try {
    showToast('Loading sample image...', 'info');
    const response = await fetch(url);
    const blob = await response.blob();
    const filename = url.substring(url.lastIndexOf('/') + 1);
    const file = new File([blob], filename, { type: 'image/jpeg' });
    processFile(file);
    showToast('Sample image loaded!', 'success');
  } catch (error) {
    console.error(error);
    showToast('Failed to load sample image.', 'error');
  }
}

function hideAll() {
  [loadingCard, resultCard, compareCard, errorCard].forEach(el => el.classList.add('hidden'));
}

// ── Loading Steps Animation ────────────────────────────────
function animateLoadingSteps() {
  const steps = [
    document.getElementById('step1'),
    document.getElementById('step2'),
    document.getElementById('step3'),
    document.getElementById('step4'),
  ];
  steps.forEach(s => { s.className = 'step'; });

  let i = 0;
  const iv = setInterval(() => {
    if (i > 0) steps[i - 1].className = 'step done';
    if (i < steps.length) {
      steps[i].className = 'step active';
      i++;
    } else {
      clearInterval(iv);
    }
  }, 600);
  return iv;
}

// ── Predict Monument ───────────────────────────────────────
async function predictMonument() {
  if (!currentFile) { showToast('No image selected.', 'error'); return; }

  hideAll();
  loadingCard.classList.remove('hidden');
  const iv = animateLoadingSteps();

  const formData = new FormData();
  formData.append('image', currentFile);

  try {
    const res  = await fetch('/predict', { method: 'POST', body: formData });
    const data = await res.json();
    clearInterval(iv);
    loadingCard.classList.add('hidden');

    if (!res.ok || data.error) {
      showError('Prediction Failed', data.error || 'Unknown error.');
      return;
    }

    currentResult = data;
    renderResult(data);
    resultCard.classList.remove('hidden');
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });

  } catch (err) {
    clearInterval(iv);
    loadingCard.classList.add('hidden');
    showError('Connection Error', 'Could not reach the server. Is Flask running?');
  }
}

// ── Render Result ──────────────────────────────────────────
function renderResult(data) {
  // Image
  document.getElementById('resultImg').src = data.image_url;

  // UNESCO badge
  const unescoTag = document.getElementById('unescoTag');
  unescoTag.classList.toggle('hidden', !data.unesco);

  // Confidence
  const pct = Math.round(data.confidence);
  document.getElementById('confPercent').textContent = pct + '%';
  const badge = document.getElementById('confidenceBadge');
  badge.style.background = pct >= 70
    ? 'linear-gradient(135deg, #68d391, #48bb78)'
    : pct >= 45
      ? 'linear-gradient(135deg, #f6ad55, #ed8936)'
      : 'linear-gradient(135deg, #fc8181, #e53e3e)';

  // Info
  document.getElementById('monumentName').textContent      = data.monument_name;
  document.getElementById('monumentLocation').textContent  = data.location;
  document.getElementById('monumentBuiltBy').textContent   = data.built_by;
  document.getElementById('monumentYear').textContent      = data.year_built;
  document.getElementById('monumentArch').textContent      = data.architecture;
  document.getElementById('monumentFee').textContent       = data.entry_fee;
  document.getElementById('monumentTimings').textContent   = data.timings;
  document.getElementById('monumentDesc').textContent      = data.description;
  document.getElementById('monumentFunFact').textContent   = data.fun_fact;
  document.getElementById('modelUsed').textContent         = data.model_used;

  // Top predictions bar chart
  const container = document.getElementById('topPredictions');
  container.innerHTML = '';
  const predictions = data.top_predictions || [];
  const maxConf = predictions.length > 0 ? predictions[0][1] : 1;

  predictions.forEach(([ label, conf ], idx) => {
    const item = document.createElement('div');
    item.className = 'pred-item';
    item.innerHTML = `
      <span class="pred-label ${idx === 0 ? 'top' : ''}">${label}</span>
      <div class="pred-bar-wrap">
        <div class="pred-bar ${idx === 0 ? 'top' : ''}" style="width: 0%"></div>
      </div>
      <span class="pred-pct">${conf.toFixed(1)}%</span>
    `;
    container.appendChild(item);
    // Animate bar width after brief delay
    setTimeout(() => {
      item.querySelector('.pred-bar').style.width = (conf / Math.max(maxConf, 1) * 100) + '%';
    }, 100 + idx * 80);
  });
}

// ── Compare All Models ─────────────────────────────────────
async function compareAllModels() {
  if (!currentFile) { showToast('No image selected.', 'error'); return; }

  compareCard.classList.add('hidden');
  hideAll();
  loadingCard.classList.remove('hidden');

  const formData = new FormData();
  formData.append('image', currentFile);

  try {
    const res  = await fetch('/all_models', { method: 'POST', body: formData });
    const data = await res.json();
    loadingCard.classList.add('hidden');

    if (!res.ok || data.error) {
      showError('Comparison Failed', data.error || 'Unknown error.');
      return;
    }

    renderComparison(data.results);
    compareCard.classList.remove('hidden');
    compareCard.scrollIntoView({ behavior: 'smooth', block: 'start' });

  } catch {
    loadingCard.classList.add('hidden');
    showError('Connection Error', 'Could not reach the server.');
  }
}

function renderComparison(results) {
  const grid = document.getElementById('compareResults');
  grid.innerHTML = '';

  // Find winner
  const best = results.reduce((a, b) => (a.confidence > b.confidence ? a : b), results[0]);

  // Prioritize Naive Bayes as it works most correctly, otherwise look for a model with 100% confidence, or fall back to the best model
  const defaultModel = results.find(item => item.model === 'Naive Bayes') || results.find(item => item.confidence === 100.0) || best;
  let activeCardElement = null;

  results.forEach(item => {
    const isWinner = item === best;
    const isActive = item === defaultModel;
    const card = document.createElement('div');
    card.className = 'compare-item' + (isWinner ? ' winner' : '');
    card.innerHTML = `
      ${isWinner ? '<div class="compare-winner-crown">🏆</div>' : ''}
      <div class="compare-model">${item.model}</div>
      <div class="compare-pred">${item.prediction}</div>
      <div class="compare-conf">${item.confidence.toFixed(1)}%</div>
    `;

    // Make card clickable to show details and update main card (with scroll)
    card.addEventListener('click', () => showCompareDetails(item, card, true));

    grid.appendChild(card);

    if (isActive) {
      activeCardElement = card;
    }
  });

  // Automatically show the details for the Naive Bayes (or best) prediction (without scroll)
  if (defaultModel) {
    showCompareDetails(defaultModel, activeCardElement, false);
  }
}

function showCompareDetails(item, cardElement, shouldScroll = false) {
  // Remove active highlight from all cards
  document.querySelectorAll('.compare-item').forEach(el => el.classList.remove('active'));

  // Highlight the clicked card
  if (cardElement) cardElement.classList.add('active');

  const panel = document.getElementById('compareDetailsPanel');
  if (!item || !item.info) {
    panel.classList.add('hidden');
    return;
  }

  // Populate comparison details panel
  document.getElementById('compSelectedModel').textContent = item.model;
  document.getElementById('compSelectedPred').textContent  = item.prediction;
  document.getElementById('compLocation').textContent      = item.info.location || 'Unknown';
  document.getElementById('compBuiltBy').textContent       = item.info.built_by || 'Unknown';
  document.getElementById('compYear').textContent          = item.info.year_built || 'Unknown';
  document.getElementById('compArch').textContent          = item.info.architecture_style || 'Unknown';
  document.getElementById('compFee').textContent           = item.info.entry_fee || 'N/A';
  document.getElementById('compTimings').textContent       = item.info.timings || 'N/A';
  document.getElementById('compDesc').textContent          = item.info.short_description || '';
  document.getElementById('compFunFact').textContent       = item.info.fun_fact || 'N/A';

  panel.classList.remove('hidden');

  // Dynamically update the main Result Card at the top of the page with the clicked model's prediction details!
  const selectedData = {
    image_url:       currentResult ? currentResult.image_url : '',
    unesco:          item.info.unesco || false,
    confidence:      item.confidence,
    monument_name:  item.prediction,
    location:       item.info.location || 'Unknown',
    built_by:       item.info.built_by || 'Unknown',
    year_built:     item.info.year_built || 'Unknown',
    architecture:   item.info.architecture_style || 'Unknown',
    entry_fee:      item.info.entry_fee || 'N/A',
    timings:        item.info.timings || 'N/A',
    description:    item.info.short_description || '',
    fun_fact:       item.info.fun_fact || 'N/A',
    model_used:     item.model,
    top_predictions: [[item.prediction, item.confidence / 100.0]]
  };

  renderResult(selectedData);

  if (shouldScroll) {
    // Smooth scroll the user back to the main Result Card to view the updated correct description!
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    // Keep focus on the comparison card on initial render
    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

// ── History ────────────────────────────────────────────────
async function loadHistory() {
  const grid = document.getElementById('historyGrid');
  grid.innerHTML = '<div class="empty-state"><div class="empty-icon">⏳</div><p>Loading…</p></div>';

  try {
    const res     = await fetch('/history');
    const history = await res.json();
    renderHistory(history);
  } catch {
    grid.innerHTML = '<div class="empty-state"><div class="empty-icon">❌</div><p>Could not load history.</p></div>';
  }
}

function renderHistory(history) {
  const grid = document.getElementById('historyGrid');
  if (!history || history.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🏛</div>
        <p>No predictions yet. Upload an image to get started!</p>
      </div>`;
    return;
  }

  grid.innerHTML = '';
  history.forEach(item => {
    const card = document.createElement('div');
    card.className = 'history-item';
    const date = new Date(item.timestamp).toLocaleDateString('en-IN', {
      day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
    });
    card.innerHTML = `
      <img src="${item.image_url}" alt="${item.monument_name}" class="history-img"
           onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22200%22 height=%22130%22><rect fill=%22%230f1629%22 width=%22200%22 height=%22130%22/><text x=%2250%%22 y=%2250%%22 text-anchor=%22middle%22 fill=%22%23718096%22 font-size=%2232%22>🏛</text></svg>'" />
      <div class="history-body">
        <div class="history-name">${item.monument_name}</div>
        <div class="history-meta">${item.location}</div>
        <div class="history-conf">${item.confidence.toFixed(1)}% confidence</div>
        <div class="history-meta">${date}</div>
      </div>
    `;
    grid.appendChild(card);
  });
}

async function clearHistory() {
  if (!confirm('Clear all prediction history?')) return;
  await fetch('/clear_history', { method: 'POST' });
  loadHistory();
  showToast('History cleared.', 'info');
}

// ── Section Navigation ─────────────────────────────────────
function showSection(name) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

  const section = document.getElementById('section-' + name);
  if (section) {
    section.classList.add('active');
    if (name === 'history') loadHistory();
  }

  const navBtns = document.querySelectorAll('.nav-btn');
  navBtns.forEach(btn => {
    if (btn.textContent.toLowerCase().includes(name.substring(0, 4).toLowerCase())) {
      btn.classList.add('active');
    }
  });
}

// ── Error Display ──────────────────────────────────────────
function showError(title, message) {
  document.getElementById('errorTitle').textContent = title;
  document.getElementById('errorMsg').textContent   = message;
  errorCard.classList.remove('hidden');
  errorCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Save Result ────────────────────────────────────────────
function saveResult() {
  if (!currentResult) return;
  const info = {
    monument:     currentResult.monument_name,
    location:     currentResult.location,
    built_by:     currentResult.built_by,
    year_built:   currentResult.year_built,
    architecture: currentResult.architecture,
    confidence:   currentResult.confidence + '%',
    timestamp:    new Date().toISOString(),
  };
  const blob = new Blob([JSON.stringify(info, null, 2)], { type: 'application/json' });
  const link = document.createElement('a');
  link.href     = URL.createObjectURL(blob);
  link.download = `monument_${info.monument.replace(/\s+/g, '_')}.json`;
  link.click();
  showToast('Result saved!', 'success');
}

// ── Toast ──────────────────────────────────────────────────
let toastTimer = null;
function showToast(message, type = 'info') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className   = `toast ${type}`;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.add('hidden'), 3000);
}
