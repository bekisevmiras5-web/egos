// Кнопка ИИ
const chatButton = document.createElement('div');
chatButton.id = 'chatButton';
chatButton.textContent = '💬';
document.body.appendChild(chatButton);

// Оверлей чата
const chatOverlay = document.createElement('div');
chatOverlay.id = 'chatOverlay';
chatOverlay.innerHTML = `
  <div id="chatBox">
    <div id="chatMessages"></div>
    <textarea id="chatInput" placeholder="Введите сообщение..."></textarea>
    <button id="sendBtn">Отправить</button>
    <button id="closeBtn">Закрыть</button>
  </div>
`;
document.body.appendChild(chatOverlay);

document.getElementById('chatButton').onclick = () => chatOverlay.style.display = 'flex';
document.getElementById('closeBtn').onclick = () => chatOverlay.style.display = 'none';

document.getElementById('sendBtn').onclick = async () => {
  const input = document.getElementById('chatInput');
  const message = input.value.trim();
  if (!message) return;

  const messagesDiv = document.getElementById('chatMessages');
  messagesDiv.innerHTML += `<div class="userMsg">${message}</div>`;
  input.value = '';

  try {
    const res = await fetch('http://localhost:3000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    const data = await res.json();
    messagesDiv.innerHTML += `<div class="aiMsg">${data.reply}</div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  } catch (err) {
    messagesDiv.innerHTML += `<div class="aiMsg error">Ошибка при получении ответа от ИИ</div>`;
    console.error(err);
  }
};
