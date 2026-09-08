/**
 * MarketMind — Main Client Dashboard & Application Script
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initMobileSidebar();
  initDashboardCharts();
  initAnalyticsCharts();
  initStrategyGenerator();
  initContentGenerator();
  initCampaignCreator();
  initEmployeeTaskActions();
});

// Theme Switcher (Dark Blue & White <-> Pixie Pink & White)
function initThemeToggle() {
  const toggleBtn = document.getElementById('themeToggleBtn');
  const savedTheme = localStorage.getItem('marketmind_theme');

  if (savedTheme === 'pink') {
    document.body.classList.add('theme-pixie-pink');
    if (toggleBtn) toggleBtn.innerHTML = '<i class="fas fa-moon"></i>';
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('theme-pixie-pink');
      const isPink = document.body.classList.contains('theme-pixie-pink');
      localStorage.setItem('marketmind_theme', isPink ? 'pink' : 'dark');
      toggleBtn.innerHTML = isPink ? '<i class="fas fa-moon"></i>' : '<i class="fas fa-magic"></i>';
    });
  }
}

// Mobile sidebar drawer
function initMobileSidebar() {
  const toggleBtn = document.getElementById('mobileSidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }
}

// Dashboard Summary Charts (Chart.js)
function initDashboardCharts() {
  const perfCanvas = document.getElementById('dashboardPerformanceChart');
  if (!perfCanvas) return;

  const ctx = perfCanvas.getContext('2d');

  // Gradient fill for sleek dark blue aesthetic
  const blueGradient = ctx.createLinearGradient(0, 0, 0, 300);
  blueGradient.addColorStop(0, 'rgba(58, 134, 255, 0.4)');
  blueGradient.addColorStop(1, 'rgba(58, 134, 255, 0.0)');

  const cyanGradient = ctx.createLinearGradient(0, 0, 0, 300);
  cyanGradient.addColorStop(0, 'rgba(0, 245, 212, 0.35)');
  cyanGradient.addColorStop(1, 'rgba(0, 245, 212, 0.0)');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      datasets: [
        {
          label: 'Reach (Impressions)',
          data: [12400, 15800, 14200, 22500, 28400, 34100, 31200],
          borderColor: '#3a86ff',
          backgroundColor: blueGradient,
          fill: true,
          tension: 0.35,
          borderWidth: 3,
          pointBackgroundColor: '#3a86ff',
          pointRadius: 4
        },
        {
          label: 'Clicks',
          data: [1100, 1450, 1320, 2400, 3210, 3950, 3600],
          borderColor: '#00f5d4',
          backgroundColor: cyanGradient,
          fill: true,
          tension: 0.35,
          borderWidth: 2.5,
          pointBackgroundColor: '#00f5d4',
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: { color: '#94a3b8', font: { family: 'Plus Jakarta Sans', size: 12 } }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b' }
        },
        y: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: '#64748b' }
        }
      }
    }
  });
}

// Deep Analytics Charts
function initAnalyticsCharts() {
  const channelCanvas = document.getElementById('channelDistributionChart');
  if (channelCanvas) {
    const ctx = channelCanvas.getContext('2d');
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Instagram', 'WhatsApp', 'YouTube', 'Google Ads', 'Email'],
        datasets: [{
          data: [42, 24, 18, 11, 5],
          backgroundColor: ['#ff006e', '#25d366', '#ff0000', '#3a86ff', '#8338ec'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#94a3b8', padding: 14 }
          }
        }
      }
    });
  }

  const spendSalesCanvas = document.getElementById('spendVsSalesChart');
  if (spendSalesCanvas) {
    const ctx = spendSalesCanvas.getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [
          {
            label: 'Spend (₹)',
            data: [6500, 8200, 9100, 8700],
            backgroundColor: 'rgba(255, 190, 11, 0.75)',
            borderRadius: 6
          },
          {
            label: 'Sales (₹)',
            data: [28000, 36500, 42400, 41300],
            backgroundColor: 'rgba(16, 185, 129, 0.85)',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { labels: { color: '#94a3b8' } }
        },
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } },
          y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#64748b' } }
        }
      }
    });
  }
}

// AI Marketing Strategy Generator Handler
function initStrategyGenerator() {
  const form = document.getElementById('strategyForm');
  const resultContainer = document.getElementById('strategyResult');
  const btn = document.getElementById('btnGenerateStrategy');

  if (!form || !resultContainer) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('strategyPrompt').value;
    const budget = document.getElementById('strategyBudget').value;
    const industry = document.getElementById('strategyIndustry').value;

    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Synthesizing AI Strategy...';
    }

    try {
      const res = await fetch('/api/strategy/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, budget, industry })
      });
      const json = await res.json();

      if (json.status === 'success') {
        const strat = json.data;
        renderStrategyView(strat);
      }
    } catch (err) {
      console.error(err);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic"></i> Generate AI Marketing Strategy';
      }
    }
  });

  function renderStrategyView(s) {
    resultContainer.style.display = 'block';
    resultContainer.scrollIntoView({ behavior: 'smooth' });

    let channelsHtml = (s.marketing_channels || []).map(c => `
      <span class="badge bg-primary text-white p-2 me-2 mb-2" style="border-radius: 8px;">
        <i class="fas fa-check-circle me-1"></i> ${c}
      </span>
    `).join('');

    let ideasHtml = (s.campaign_ideas || []).map(idea => `
      <div class="card mb-3" style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(58, 134, 255, 0.2);">
        <div class="card-body">
          <h5 class="text-white fw-bold"><i class="fas fa-bullhorn text-cyan me-2"></i>${idea.name}</h5>
          <p class="text-light mb-2"><strong>Hook:</strong> "${idea.hook}"</p>
          <div class="d-flex justify-content-between text-secondary small">
            <span><strong>Platform:</strong> ${idea.platform}</span>
            <span class="text-emerald"><strong>Expected:</strong> ${idea.expected_outcome}</span>
          </div>
        </div>
      </div>
    `).join('');

    let budgetRows = (s.budget_distribution || []).map(b => `
      <tr>
        <td class="text-white fw-bold">${b.channel}</td>
        <td><span class="status-pill inprogress">${b.percentage}%</span></td>
        <td class="text-amber fw-bold">${b.amount}</td>
        <td class="text-secondary">${b.purpose}</td>
      </tr>
    `).join('');

    let goalsHtml = (s.marketing_goals || []).map(g => `
      <li class="mb-2 text-light"><i class="fas fa-flag-checkered text-cyan me-2"></i>${g}</li>
    `).join('');

    resultContainer.innerHTML = `
      <div class="card mb-4" style="border-left: 4px solid var(--accent-cyan);">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="text-white"><i class="fas fa-brain text-cyan me-2"></i>Generated Strategy Roadmap</h3>
            <span class="badge bg-cyan text-dark fw-bold px-3 py-2">AI-Engine Verified</span>
          </div>
          <p class="lead text-light mb-4">${s.summary || ''}</p>

          <div class="row g-4">
            <div class="col-md-6">
              <div class="p-3 rounded" style="background: rgba(10, 15, 29, 0.6); border: 1px solid var(--border-color);">
                <h5 class="text-cyan mb-3"><i class="fas fa-users me-2"></i>Target Audience Profile</h5>
                <p class="text-secondary">${s.target_audience}</p>
              </div>
            </div>
            <div class="col-md-6">
              <div class="p-3 rounded" style="background: rgba(10, 15, 29, 0.6); border: 1px solid var(--border-color);">
                <h5 class="text-cyan mb-3"><i class="fas fa-share-alt me-2"></i>Recommended Channels</h5>
                <div class="d-flex flex-wrap">${channelsHtml}</div>
              </div>
            </div>
          </div>

          <h4 class="text-white mt-4 mb-3"><i class="fas fa-lightbulb text-amber me-2"></i>Campaign Execution Concepts</h4>
          ${ideasHtml}

          <h4 class="text-white mt-4 mb-3"><i class="fas fa-coins text-amber me-2"></i>Suggested Budget Distribution</h4>
          <div class="table-responsive">
            <table class="table-custom">
              <thead>
                <tr>
                  <th>Marketing Channel</th>
                  <th>Split %</th>
                  <th>Allocated Amount</th>
                  <th>Strategy Focus</th>
                </tr>
              </thead>
              <tbody>${budgetRows}</tbody>
            </table>
          </div>

          <h4 class="text-white mt-4 mb-3"><i class="fas fa-bullseye text-cyan me-2"></i>Core Marketing Goals</h4>
          <ul class="list-unstyled">${goalsHtml}</ul>
        </div>
      </div>
    `;
  }
}

// AI Content Generator Studio
function initContentGenerator() {
  const form = document.getElementById('contentGenForm');
  const resultBox = document.getElementById('contentResultBox');
  const submitBtn = document.getElementById('btnGenContent');

  if (!form || !resultBox) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const contentType = document.getElementById('contentTypeSelect').value;
    const topic = document.getElementById('contentTopic').value;
    const tone = document.getElementById('contentTone').value;
    const product = document.getElementById('contentProduct').value;

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Writing Copy...';
    }

    try {
      const res = await fetch('/api/content/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ contentType, topic, tone, product })
      });
      const data = await res.json();

      if (data.status === 'success') {
        renderGeneratedContent(data.data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-sparkles"></i> Generate AI Content';
      }
    }
  });

  function renderGeneratedContent(c) {
    resultBox.style.display = 'block';

    const tagsHtml = (c.hashtags || []).map(t => `<span class="badge bg-secondary me-1 mb-1">${t}</span>`).join(' ');
    const varsHtml = (c.variations || []).map((v, i) => `
      <div class="p-3 mb-2 rounded" style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color);">
        <div class="d-flex justify-content-between mb-1">
          <strong class="text-secondary small">Variation #${i + 1}</strong>
          <button class="btn btn-sm btn-outline py-0 px-2" onclick="navigator.clipboard.writeText(\`${v.replace(/`/g, '\\`')}\`); alert('Copied!')">
            <i class="fas fa-copy"></i>
          </button>
        </div>
        <p class="text-light mb-0">${v.replace(/\n/g, '<br/>')}</p>
      </div>
    `).join('');

    resultBox.innerHTML = `
      <div class="card" style="border: 1px solid var(--accent-cyan);">
        <div class="card-header">
          <h4 class="card-title text-cyan"><i class="fas fa-check-circle"></i> ${c.content_type} Ready!</h4>
          <button class="btn btn-sm btn-cyan" onclick="navigator.clipboard.writeText(document.getElementById('primaryCopyTarget').innerText); alert('Copied to clipboard!')">
            <i class="fas fa-copy"></i> Copy Primary
          </button>
        </div>
        <div class="card-body">
          <div class="p-3 mb-4 rounded" style="background: rgba(10, 15, 29, 0.8); border: 1px solid var(--border-color);">
            <h6 class="text-cyan text-uppercase small">Primary Recommended Copy</h6>
            <div id="primaryCopyTarget" class="text-white fs-6 py-2" style="white-space: pre-wrap;">${c.primary_content}</div>
          </div>

          <div class="mb-3">
            <h6 class="text-secondary text-uppercase small">High-Converting Variations</h6>
            ${varsHtml}
          </div>

          <div class="mb-3">
            <h6 class="text-secondary text-uppercase small">Recommended Hashtags</h6>
            <div>${tagsHtml}</div>
          </div>

          <div class="alert alert-info py-2 small" style="background: rgba(58, 134, 255, 0.15); border-color: rgba(58, 134, 255, 0.3); color: #e2e8f0;">
            <i class="fas fa-lightbulb text-amber me-1"></i> <strong>Pro Strategy:</strong> ${c.pro_tip || ''}
          </div>
        </div>
      </div>
    `;
  }
}

// Campaign Creator Form
function initCampaignCreator() {
  const form = document.getElementById('campaignCreateForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('campTitle').value;
    const channel = document.getElementById('campChannel').value;
    const target = document.getElementById('campTarget').value;
    const budget = document.getElementById('campBudget').value;
    const duration = document.getElementById('campDuration').value;

    try {
      const res = await fetch('/api/campaigns/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, channel, target, budget, duration })
      });
      const data = await res.json();
      if (data.status === 'success') {
        alert('Campaign created successfully!');
        window.location.reload();
      }
    } catch (err) {
      console.error(err);
    }
  });
}

// Part-Time Employee Task Accept & Proof Submission
function initEmployeeTaskActions() {
  window.acceptTask = async function(taskId) {
    if (!confirm("Are you sure you want to take up this marketing task?")) return;
    try {
      const res = await fetch(`/api/employee/task/${taskId}/accept`, { method: 'POST' });
      const data = await res.json();
      if (data.status === 'success') {
        alert('Task assigned to you! Check "My Active Tasks" below.');
        window.location.reload();
      }
    } catch (err) {
      console.error(err);
    }
  };

  window.submitProofModal = function(taskId, taskTitle) {
    const proofUrl = prompt(`Enter proof link (Instagram post/reel URL, cloud drive folder, etc.) for "${taskTitle}":`);
    if (!proofUrl) return;
    const proofNotes = prompt("Enter any comments or reach numbers achieved:");

    fetch(`/api/employee/task/${taskId}/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ proof_url: proofUrl, proof_text: proofNotes || '' })
    }).then(res => res.json()).then(data => {
      if (data.status === 'success') {
        alert("Proof submitted successfully! The business owner has been notified.");
        window.location.reload();
      }
    });
  };
}
