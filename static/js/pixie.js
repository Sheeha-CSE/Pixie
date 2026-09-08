/**
 * MarketMind — Pixie AI Companion Engine
 * Handles:
 * - Canvas Realistic Glitter & Sparkle Snowfall
 * - Mascot Eye-Blinking & Curious State Machine
 * - Welcome Slideshow (Think, Learn, Grow)
 * - Microphone Voice Input (Speech-to-Text)
 * - Voice Output (Text-to-Speech)
 * - Dynamic Context Background Switcher
 * - Media Generator (Pictures & Videos)
 * - File Uploads (Images & Videos)
 */

class PixieAssistant {
  constructor() {
    this.modal = document.getElementById('pixieModal');
    this.triggerBtn = document.getElementById('pixieTrigger');
    this.closeBtn = document.getElementById('closePixieModal');
    this.chatBody = document.getElementById('pixieChatBody');
    this.input = document.getElementById('pixieInput');
    this.sendBtn = document.getElementById('btnPixieSend');
    this.micBtn = document.getElementById('btnPixieMic');
    this.ttsBtn = document.getElementById('btnPixieTTS');
    this.langSelect = document.getElementById('pixieLanguage');
    this.bgLayer = document.getElementById('pixieBgLayer');
    this.sparkleCanvas = document.getElementById('pixieSparkleCanvas');
    this.waitingBadge = document.getElementById('mascotWaiting');
    this.mascotWrap = document.querySelector('.mascot-avatar-frame');
    
    // File upload elements
    this.fileInput = document.getElementById('pixieMediaUpload');
    this.fileUploadBtn = document.getElementById('btnPixieUpload');
    this.previewTray = document.getElementById('uploadPreviewTray');
    this.currentFile = null;
    this.currentFileType = null;

    // Slideshow elements
    this.slideshowOverlay = document.getElementById('pixieSlideshow');
    this.btnStartChat = document.getElementById('btnStartChat');
    this.btnNextSlide = document.getElementById('btnNextSlide');
    this.slideDots = document.querySelectorAll('.slide-dot');
    this.currentSlide = 0;
    this.slidesData = [
      {
        badge: "✨ Welcome to Pixie",
        title: "Your Creative AI <span>Companion</span>",
        desc: "I'm Pixie! Inspired by playful curiosity and built with advanced AI to empower your business and college life.",
        features: [
          { icon: "fas fa-lightbulb", text: "Think Deeply" },
          { icon: "fas fa-graduation-cap", text: "Learn Daily" },
          { icon: "fas fa-chart-line", text: "Grow Fast" }
        ]
      },
      {
        badge: "🧠 Think",
        title: "AI Marketing <span>Strategies</span>",
        desc: "Enter your business idea, and I'll generate full audience profiles, channel roadmaps, budget splits in ₹, and goals!",
        features: [
          { icon: "fab fa-instagram", text: "Social Reels" },
          { icon: "fab fa-whatsapp", text: "WhatsApp Blasts" },
          { icon: "fas fa-bullseye", text: "Targeted Ads" }
        ]
      },
      {
        badge: "🎓 Learn",
        title: "Educational & <span>College Hub</span>",
        desc: "Ask me anything about college admissions, campus fests, study-work balance, or student marketing gigs!",
        features: [
          { icon: "fas fa-book-reader", text: "Exam Guidance" },
          { icon: "fas fa-users", text: "Campus Clubs" },
          { icon: "fas fa-award", text: "Fest Marketing" }
        ]
      },
      {
        badge: "🚀 Grow",
        title: "Empowering <span>Students & Owners</span>",
        desc: "Connects business owners with enthusiastic part-time student marketers. Earn rewards, boost engagement, and create viral campaigns!",
        features: [
          { icon: "fas fa-wallet", text: "Student Stipends" },
          { icon: "fas fa-magic", text: "Glitter AI" },
          { icon: "fas fa-globe", text: "Multi-Language" }
        ]
      }
    ];

    // State
    this.isGenerating = false;
    this.voiceEnabled = true;
    this.chatHistory = [];
    this.recognition = null;
    this.sparkles = [];
    this.animFrameId = null;

    this.backgroundThemes = {
      campus: "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=1200&auto=format&fit=crop&q=80",
      fashion: "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=1200&auto=format&fit=crop&q=80",
      growth: "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&auto=format&fit=crop&q=80",
      tech: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200&auto=format&fit=crop&q=80",
      creative: "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=1200&auto=format&fit=crop&q=80",
      general: "https://images.unsplash.com/photo-1557804506-669a67965ba0?w=1200&auto=format&fit=crop&q=80"
    };

    this.init();
  }

  init() {
    this.setupEventListeners();
    this.initSpeechRecognition();
    this.initSparkleCanvas();
    this.initMascotBlinks();
    this.loadChatHistory();
  }

  setupEventListeners() {
    if (this.triggerBtn) {
      this.triggerBtn.addEventListener('click', () => this.openModal());
    }
    if (this.closeBtn) {
      this.closeBtn.addEventListener('click', () => this.closeModal());
    }

    // Modal background click to close
    if (this.modal) {
      this.modal.addEventListener('click', (e) => {
        if (e.target === this.modal) this.closeModal();
      });
    }

    // Send on click or Enter
    if (this.sendBtn) {
      this.sendBtn.addEventListener('click', () => this.sendMessage());
    }
    if (this.input) {
      this.input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });

      // Typing animation for curious eyes
      this.input.addEventListener('input', () => {
        if (this.mascotWrap) {
          this.mascotWrap.classList.add('mascot-curious');
          clearTimeout(this.typingTimer);
          this.typingTimer = setTimeout(() => {
            this.mascotWrap.classList.remove('mascot-curious');
          }, 1800);
        }
      });
    }

    // Mic button
    if (this.micBtn) {
      this.micBtn.addEventListener('click', () => this.toggleMic());
    }

    // Voice TTS Toggle
    if (this.ttsBtn) {
      this.ttsBtn.addEventListener('click', () => {
        this.voiceEnabled = !this.voiceEnabled;
        this.ttsBtn.classList.toggle('active', this.voiceEnabled);
        if (this.voiceEnabled) {
          this.speakText("Voice output enabled! Pixie is ready to talk ✨");
        }
      });
    }

    // File upload
    if (this.fileUploadBtn && this.fileInput) {
      this.fileUploadBtn.addEventListener('click', () => this.fileInput.click());
      this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    }

    // Slideshow navigation
    if (this.btnStartChat) {
      this.btnStartChat.addEventListener('click', () => this.dismissSlideshow());
    }
    if (this.btnNextSlide) {
      this.btnNextSlide.addEventListener('click', () => this.nextSlide());
    }
    this.slideDots.forEach((dot, index) => {
      dot.addEventListener('click', () => this.goToSlide(index));
    });
  }

  // --- Mascot Eyes & Curious Waiting ---
  initMascotBlinks() {
    // Blinks are also handled by CSS animations on `.mascot-eyelid`
    // We add natural random curious looks
    setInterval(() => {
      if (!this.isGenerating && this.mascotWrap) {
        if (Math.random() > 0.4) {
          this.mascotWrap.classList.add('mascot-curious');
          setTimeout(() => {
            this.mascotWrap.classList.remove('mascot-curious');
          }, 2400);
        }
      }
    }, 5000);
  }

  // --- Slideshow Methods ---
  nextSlide() {
    this.goToSlide((this.currentSlide + 1) % this.slidesData.length);
  }

  goToSlide(index) {
    this.currentSlide = index;
    const data = this.slidesData[index];
    const badge = document.getElementById('slideBadge');
    const title = document.getElementById('slideTitle');
    const desc = document.getElementById('slideDesc');
    const featContainer = document.getElementById('slideFeatures');

    if (badge) badge.innerText = data.badge;
    if (title) title.innerHTML = data.title;
    if (desc) desc.innerText = data.desc;
    if (featContainer) {
      featContainer.innerHTML = data.features.map(f => `
        <div class="feature-pill">
          <i class="${f.icon}"></i>
          <span>${f.text}</span>
        </div>
      `).join('');
    }

    this.slideDots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });

    if (this.btnNextSlide) {
      this.btnNextSlide.innerText = index === this.slidesData.length - 1 ? "Start Chatting ✨" : "Next →";
    }
    if (index === this.slidesData.length - 1 && this.btnNextSlide) {
      this.btnNextSlide.onclick = () => this.dismissSlideshow();
    }
  }

  dismissSlideshow() {
    if (this.slideshowOverlay) {
      this.slideshowOverlay.classList.add('hidden');
      sessionStorage.setItem('pixie_slideshow_seen', 'true');
    }
  }

  openModal() {
    if (this.modal) {
      this.modal.classList.add('open');
      document.body.style.overflow = 'hidden';
      if (!sessionStorage.getItem('pixie_slideshow_seen')) {
        this.goToSlide(0);
      } else if (this.slideshowOverlay) {
        this.slideshowOverlay.classList.add('hidden');
      }
      setTimeout(() => this.input && this.input.focus(), 300);
    }
  }

  closeModal() {
    if (this.modal) {
      this.modal.classList.remove('open');
      document.body.style.overflow = '';
      this.stopSparkles();
    }
  }

  // --- Realistic Glitter & Sparkle Snowfall Canvas ---
  initSparkleCanvas() {
    if (!this.sparkleCanvas) return;
    this.ctx = this.sparkleCanvas.getContext('2d');
    this.resizeCanvas();
    window.addEventListener('resize', () => this.resizeCanvas());
  }

  resizeCanvas() {
    if (!this.sparkleCanvas) return;
    this.sparkleCanvas.width = this.sparkleCanvas.parentElement.clientWidth;
    this.sparkleCanvas.height = this.sparkleCanvas.parentElement.clientHeight;
  }

  startSparkles() {
    if (!this.sparkleCanvas) return;
    this.isGenerating = true;
    this.sparkles = [];
    this.resizeCanvas();

    const w = this.sparkleCanvas.width;
    const colors = ['#FFFFFF', '#FFD166', '#FF758F', '#00F5D4', '#FFF0F5', '#FFB703'];

    // Spawn 70 realistic sparkling particles
    for (let i = 0; i < 70; i++) {
      this.sparkles.push({
        x: Math.random() * w,
        y: Math.random() * -200,
        size: Math.random() * 5 + 2,
        speedY: Math.random() * 2.5 + 1.2,
        speedX: (Math.random() - 0.5) * 1.2,
        rotation: Math.random() * 360,
        rotSpeed: (Math.random() - 0.5) * 5,
        color: colors[Math.floor(Math.random() * colors.length)],
        opacity: Math.random() * 0.7 + 0.3,
        twinkleSpeed: Math.random() * 0.08 + 0.02,
        twinklePhase: Math.random() * Math.PI * 2,
        type: Math.random() > 0.4 ? 'star' : 'dust'
      });
    }

    if (this.waitingBadge) this.waitingBadge.classList.add('active');
    if (this.mascotWrap) this.mascotWrap.classList.add('mascot-curious');

    const animate = () => {
      this.ctx.clearRect(0, 0, this.sparkleCanvas.width, this.sparkleCanvas.height);

      this.sparkles.forEach(p => {
        p.y += p.speedY;
        p.x += p.speedX + Math.sin(p.y * 0.02) * 0.8;
        p.rotation += p.rotSpeed;
        p.twinklePhase += p.twinkleSpeed;
        const currentOpacity = Math.max(0.15, Math.min(1, p.opacity + Math.sin(p.twinklePhase) * 0.35));

        this.ctx.save();
        this.ctx.translate(p.x, p.y);
        this.ctx.rotate((p.rotation * Math.PI) / 180);
        this.ctx.globalAlpha = currentOpacity;
        this.ctx.fillStyle = p.color;

        if (p.type === 'star') {
          // Draw a sparkling 4-point star
          this.drawSparkleStar(this.ctx, 0, 0, 4, p.size * 1.8, p.size * 0.4);
        } else {
          // Soft glowing circular diamond dust
          this.ctx.beginPath();
          this.ctx.arc(0, 0, p.size * 0.8, 0, Math.PI * 2);
          this.ctx.fill();
        }
        this.ctx.restore();

        // Respawn when falling off screen
        if (p.y > this.sparkleCanvas.height + 20) {
          p.y = -20;
          p.x = Math.random() * this.sparkleCanvas.width;
        }
      });

      if (this.isGenerating) {
        this.animFrameId = requestAnimationFrame(animate);
      } else {
        this.ctx.clearRect(0, 0, this.sparkleCanvas.width, this.sparkleCanvas.height);
      }
    };

    this.animFrameId = requestAnimationFrame(animate);
  }

  drawSparkleStar(ctx, cx, cy, spikes, outerRadius, innerRadius) {
    let rot = (Math.PI / 2) * 3;
    let x = cx;
    let y = cy;
    let step = Math.PI / spikes;

    ctx.beginPath();
    ctx.moveTo(cx, cy - outerRadius);
    for (let i = 0; i < spikes; i++) {
      x = cx + Math.cos(rot) * outerRadius;
      y = cy + Math.sin(rot) * outerRadius;
      ctx.lineTo(x, y);
      rot += step;

      x = cx + Math.cos(rot) * innerRadius;
      y = cy + Math.sin(rot) * innerRadius;
      ctx.lineTo(x, y);
      rot += step;
    }
    ctx.lineTo(cx, cy - outerRadius);
    ctx.closePath();
    ctx.fill();
  }

  stopSparkles() {
    this.isGenerating = false;
    if (this.animFrameId) cancelAnimationFrame(this.animFrameId);
    if (this.ctx && this.sparkleCanvas) {
      this.ctx.clearRect(0, 0, this.sparkleCanvas.width, this.sparkleCanvas.height);
    }
    if (this.waitingBadge) this.waitingBadge.classList.remove('active');
    if (this.mascotWrap) this.mascotWrap.classList.remove('mascot-curious');
  }

  // --- Speech Recognition (Microphone) ---
  initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;

      this.recognition.onstart = () => {
        if (this.micBtn) this.micBtn.classList.add('listening');
      };

      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (this.input) {
          this.input.value = transcript;
          this.sendMessage();
        }
      };

      this.recognition.onerror = () => {
        if (this.micBtn) this.micBtn.classList.remove('listening');
      };

      this.recognition.onend = () => {
        if (this.micBtn) this.micBtn.classList.remove('listening');
      };
    } else {
      if (this.micBtn) this.micBtn.title = "Speech recognition not supported in this browser";
    }
  }

  toggleMic() {
    if (!this.recognition) {
      alert("Speech-to-text is available in Chrome/Edge. Please type your message!");
      return;
    }
    try {
      this.recognition.start();
    } catch (e) {
      this.recognition.stop();
    }
  }

  speakText(text) {
    if (!this.voiceEnabled || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    // Clean markdown for speech
    const cleanText = text.replace(/[*#_`~\[\]]/g, '').slice(0, 260);
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.pitch = 1.25; // Playful, cute tone
    utterance.rate = 1.05;
    window.speechSynthesis.speak(utterance);
  }

  // --- Dynamic Background Switcher ---
  changeBackground(topicCategory) {
    if (!this.bgLayer) return;
    const url = this.backgroundThemes[topicCategory] || this.backgroundThemes.general;
    this.bgLayer.style.backgroundImage = `url('${url}')`;
    this.bgLayer.classList.add('animating');
  }

  // --- File Upload Handling ---
  handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    this.currentFile = file;
    this.currentFileType = file.type.startsWith('video') ? 'video' : 'image';

    const reader = new FileReader();
    reader.onload = (event) => {
      const previewImg = document.getElementById('previewImg');
      const previewName = document.getElementById('previewFileName');
      if (previewImg) previewImg.src = event.target.result;
      if (previewName) previewName.innerText = file.name;
      if (this.previewTray) this.previewTray.classList.add('active');
    };
    reader.readAsDataURL(file);
  }

  clearFileUpload() {
    this.currentFile = null;
    this.currentFileType = null;
    if (this.fileInput) this.fileInput.value = '';
    if (this.previewTray) this.previewTray.classList.remove('active');
  }

  // --- Messaging Pipeline ---
  async sendMessage(customText = null) {
    const text = customText || (this.input ? this.input.value.trim() : "");
    if (!text && !this.currentFile) return;

    if (this.input) this.input.value = "";

    let mediaDataUrl = null;
    let mediaType = this.currentFileType;

    if (this.currentFile) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        mediaDataUrl = e.target.result;
        this.renderMessage('user', text || "Shared media", mediaDataUrl, mediaType);
        this.clearFileUpload();
        await this.queryPixieBackend(text, mediaDataUrl, mediaType);
      };
      reader.readAsDataURL(this.currentFile);
      return;
    }

    this.renderMessage('user', text);
    await this.queryPixieBackend(text);
  }

  renderMessage(sender, text, mediaUrl = null, mediaType = null, mediaGrid = null, quickChips = null) {
    if (!this.chatBody) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${sender}`;

    const avatarHtml = sender === 'pixie'
      ? `<div class="msg-avatar"><img src="/static/assets/mascot.svg" style="width:28px; height:28px; border-radius:50%;" alt="Pixie"/></div>`
      : `<div class="msg-avatar"><i class="fas fa-user"></i></div>`;

    let mediaHtml = '';
    if (mediaUrl) {
      if (mediaType === 'video') {
        mediaHtml = `<video controls style="max-width: 100%; border-radius: 12px; margin-top: 10px;" src="${mediaUrl}"></video>`;
      } else {
        mediaHtml = `<img src="${mediaUrl}" style="max-width: 100%; max-height: 240px; border-radius: 12px; margin-top: 10px; object-fit: cover;" alt="User upload" />`;
      }
    }

    let embedGridHtml = '';
    if (mediaGrid && mediaGrid.length > 0) {
      embedGridHtml = `<div class="media-embed-grid">` + mediaGrid.map(item => `
        <div class="media-embed-card">
          ${item.type === 'video'
            ? `<video controls src="${item.sample_url}"></video>`
            : `<img src="${item.sample_url}" alt="${item.title}" loading="lazy"/>`
          }
          <div class="media-embed-info">
            <i class="fas ${item.type === 'video' ? 'fa-video' : 'fa-image'} text-primary me-1"></i>
            ${item.title}
          </div>
        </div>
      `).join('') + `</div>`;
    }

    let chipsHtml = '';
    if (quickChips && quickChips.length > 0) {
      chipsHtml = `<div class="quick-chips-row">` + quickChips.map(c => `
        <button class="quick-chip" onclick="window.pixieBot.sendMessage('${c.replace(/'/g, "\\'")}')">${c}</button>
      `).join('') + `</div>`;
    }

    // Markdown conversion (bold, lists, emojis)
    const formattedText = this.formatMarkdown(text);

    msgDiv.innerHTML = `
      ${avatarHtml}
      <div class="msg-content-wrap">
        <div class="msg-bubble">
          ${formattedText}
          ${mediaHtml}
          ${embedGridHtml}
        </div>
        ${chipsHtml}
      </div>
    `;

    this.chatBody.appendChild(msgDiv);
    this.chatBody.scrollTop = this.chatBody.scrollHeight;
  }

  formatMarkdown(text) {
    if (!text) return "";
    let html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/^### (.*$)/gim, '<h4 class="mt-2 mb-1" style="font-size:1.05rem; font-weight:700;">$1</h4>')
      .replace(/^## (.*$)/gim, '<h3 class="mt-2 mb-1" style="font-size:1.15rem; font-weight:800;">$1</h3>')
      .replace(/^\- (.*$)/gim, '<div style="margin-left:14px; margin-bottom:4px;">• $1</div>')
      .replace(/\n/g, '<br/>');
    return html;
  }

  async queryPixieBackend(userMessage, mediaUrl = null, mediaType = null) {
    this.startSparkles();

    const selectedLang = this.langSelect ? this.langSelect.value : 'English';

    try {
      const response = await fetch('/api/pixie/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userMessage,
          language: selectedLang,
          history: this.chatHistory,
          media_url: mediaUrl,
          media_type: mediaType
        })
      });

      const data = await response.json();
      this.stopSparkles();

      if (data.status === 'success') {
        const payload = data.data;

        // Change dynamic background
        if (payload.topic_category) {
          this.changeBackground(payload.topic_category);
        }

        // Render response
        this.renderMessage(
          'pixie',
          payload.reply,
          null,
          null,
          payload.suggested_media,
          payload.quick_followups
        );

        // Pixie speech
        this.speakText(payload.reply);

        // Update session history
        this.chatHistory.push({ sender: 'user', message: userMessage });
        this.chatHistory.push({ sender: 'pixie', message: payload.reply });
        localStorage.setItem('pixie_recent_chat', JSON.stringify(this.chatHistory.slice(-10)));
      } else {
        this.renderMessage('pixie', "✨ Oops! Pixie hit a little snag. Could you try asking that again?");
      }
    } catch (err) {
      this.stopSparkles();
      console.error(err);
      this.renderMessage('pixie', "✨ Pixie is thinking fast! Here is an instant answer: For maximum engagement, share authentic student stories and short videos right around 7 PM!");
    }
  }

  loadChatHistory() {
    const saved = localStorage.getItem('pixie_recent_chat');
    if (saved) {
      try {
        this.chatHistory = JSON.parse(saved);
        if (this.chatHistory.length > 0) {
          this.chatHistory.forEach(item => {
            this.renderMessage(item.sender, item.message);
          });
        }
      } catch (e) {
        this.chatHistory = [];
      }
    } else {
      // First welcome message
      this.renderMessage(
        'pixie',
        "✨ **Welcome to Pixie!** 💖\n\nI'm your 24/7 AI Marketing & Campus Life buddy! Ask me about high-converting campaign strategies, college fest promotions, or student part-time marketing gigs!",
        null,
        null,
        null,
        [
          "How to launch a college fest clothing campaign?",
          "Best marketing strategies for students",
          "Explain competitor differentiation in marketing"
        ]
      );
    }
  }
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
  window.pixieBot = new PixieAssistant();
});
