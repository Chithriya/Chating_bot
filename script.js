// ===== NIELIT CHATBOT FRONTEND SCRIPT =====

let isOpen = false;
let isLoading = false;

function toggleChat() {
  const chatbox = document.getElementById('chatbox');
  const iconChat = document.querySelector('.icon-chat');
  const iconClose = document.querySelector('.icon-close');

  isOpen = !isOpen;

  if (isOpen) {
    chatbox.style.display = 'flex';
    iconChat.style.display = 'none';
    iconClose.style.display = 'block';
    document.getElementById('userInput').focus();
    scrollToBottom();
  } else {
    chatbox.style.display = 'none';
    iconChat.style.display = 'block';
    iconClose.style.display = 'none';
  }
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function sendQuick(text) {
  document.getElementById('userInput').value = text;
  sendMessage();
}

function scrollToBottom() {
  const chatBody = document.getElementById('chatBody');
  setTimeout(() => {
    chatBody.scrollTop = chatBody.scrollHeight;
  }, 50);
}

function getTime() {
  return new Date().toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
}

function appendUserMessage(text) {
  const chatBody = document.getElementById('chatBody');
  const wrapper = document.createElement('div');
  wrapper.className = 'message-wrapper user';
  wrapper.innerHTML = `
    <div class="user-message">${escapeHtml(text)}</div>
    <div class="msg-time">${getTime()}</div>
  `;
  chatBody.appendChild(wrapper);
  scrollToBottom();
}

function appendBotMessage(text, isError = false) {
  const chatBody = document.getElementById('chatBody');
  const wrapper = document.createElement('div');
  wrapper.className = 'message-wrapper bot';

  const formatted = formatBotText(text);

  wrapper.innerHTML = `
    <div class="bot-message ${isError ? 'error-message' : ''}">${formatted}<span class="source-tag">NIELIT AI</span></div>
    <div class="msg-time">${getTime()}</div>
  `;
  chatBody.appendChild(wrapper);
  scrollToBottom();
}

function formatBotText(text) {
  // Convert markdown-like formatting to HTML
  return escapeHtml(text)
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^/, '<p>')
    .replace(/$/, '</p>');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

function showTyping() {
  document.getElementById('typingIndicator').classList.remove('hidden');
  scrollToBottom();
}

function hideTyping() {
  document.getElementById('typingIndicator').classList.add('hidden');
}

function setLoading(state) {
  isLoading = state;
  const btn = document.getElementById('sendBtn');
  const input = document.getElementById('userInput');
  btn.disabled = state;
  input.disabled = state;
}

async function sendMessage() {
  if (isLoading) return;

  const input = document.getElementById('userInput');
  const message = input.value.trim();
  if (!message) return;

  input.value = '';
  appendUserMessage(message);
  showTyping();
  setLoading(true);

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    hideTyping();
    appendBotMessage(data.reply || 'Sorry, I could not process your request.');
  } catch (err) {
    hideTyping();
    appendBotMessage(
      'Sorry, I\'m having trouble connecting right now. Please try again in a moment, or contact NIELIT Chennai directly.',
      true
    );
    console.error('Chat error:', err);
  } finally {
    setLoading(false);
    input.focus();
  }
}

function clearChat() {
  const chatBody = document.getElementById('chatBody');
  chatBody.innerHTML = `
    <div class="welcome-message">
      <div class="welcome-avatar">🎓</div>
      <div class="welcome-text">
        <strong>Chat cleared! How can I help you?</strong>
        <p>Ask me anything about NIELIT Chennai courses, syllabus, exam patterns, admissions, and more.</p>
      </div>
    </div>
  `;
}
