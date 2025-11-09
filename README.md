<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Egos — умный агроассистент</title>

<!-- Leaflet -->
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

<style>
:root{
  --bg:#f4f4f4; --fg:#222; --accent:#2e8b57; --card:#fff;
}
[data-theme="dark"]{
  --bg:#0f1720; --fg:#e6eef8; --accent:#3ddc84; --card:#0b1220;
}
[data-theme="green"]{
  --bg:#eaf8f0; --fg:#12322b; --accent:#2e8b57; --card:#f8fff9;
}
[data-theme="field"]{
  --bg:#fff7ec; --fg:#2b2618; --accent:#8b5a2b; --card:#fffaf3;
}

*{box-sizing:border-box;font-family:Inter, Poppins, system-ui, sans-serif}
html,body{height:100%;margin:0;background:var(--bg);color:var(--fg);scroll-behavior:smooth}
header{position:fixed;top:0;left:0;right:0;display:flex;align-items:center;justify-content:space-between;padding:12px 20px;background:rgba(255,255,255,0.75);backdrop-filter: blur(6px);z-index:1000;border-bottom:1px solid rgba(0,0,0,0.05)}
header h1{margin:0;color:var(--accent)}
nav ul{display:flex;gap:14px;list-style:none;margin:0;padding:0}
nav a{color:var(--fg);text-decoration:none;font-weight:500}
.container{padding:100px 6% 40px;max-width:1200px;margin:0 auto}
section{margin-bottom:48px}
#map{height:60vh;border-radius:10px;box-shadow:0 8px 30px rgba(0,0,0,0.08)}
#weather{margin-top:14px;padding:12px;border-radius:10px;background:var(--card);box-shadow:0 6px 18px rgba(0,0,0,0.06)}
.train{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end}
.wagon{width:180px;padding:12px;border-radius:10px;background:var(--card);box-shadow:0 6px 18px rgba(0,0,0,0.06);transition:transform .25s}
.wagon:hover{transform:translateY(-8px)}
.wagon img{width:100%;height:120px;object-fit:cover;border-radius:8px}
footer{text-align:center;padding:20px;color:var(--fg)}

/* Chat */
.chat-toggle{position:fixed;right:18px;bottom:18px;background:var(--accent);color:white;border:none;border-radius:999px;padding:12px 16px;cursor:pointer;box-shadow:0 10px 30px rgba(0,0,0,0.2);z-index:2000}
.chat-window{position:fixed;right:18px;bottom:76px;width:360px;max-width:92vw;height:520px;background:var(--card);border-radius:12px;box-shadow:0 20px 40px rgba(0,0,0,0.25);display:flex;flex-direction:column;overflow:hidden;z-index:2000}
.chat-header{padding:12px 14px;border-bottom:1px solid rgba(0,0,0,0.06);display:flex;align-items:center;justify-content:space-between}
.chat-body{flex:1;padding:12px;overflow:auto}
.msg{margin-bottom:10px;max-width:85%;}
.msg.user{align-self:flex-end;background:var(--accent);color:white;padding:8px 12px;border-radius:12px 12px 8px 12px}
.msg.bot{align-self:flex-start;background:rgba(0,0,0,0.06);color:var(--fg);padding:8px 12px;border-radius:12px 12px 12px 8px}
.chat-input{display:flex;padding:10px;border-top:1px solid rgba(0,0,0,0.06)}
.chat-input input{flex:1;padding:8px;border-radius:8px;border:1px solid rgba(0,0,0,0.08)}
.chat-input button{margin-left:8px;padding:8px 12px;border-radius:8px;border:none;background:var(--accent);color:white;cursor:pointer}

/* Theme & QR */
.controls{display:flex;gap:8px;align-items:center}
.theme-btn{padding:6px 10px;border-radius:8px;border:1px solid rgba(0,0,0,0.06);cursor:pointer;background:transparent}
@media (max-width:640px){header{padding:10px} .chat-window{width:92vw;right:4%}}
</style>
</head>
<body data-theme="green">

<header>
  <h1>Egos</h1>
  <nav>
    <ul>
      <li><a href="#map-section">Главная</a></li>
      <li><a href="#team">Команда</a></li>
      <li><a href="#about">О проекте</a></li>
      <li><a href="#channels">Каналы</a></li>
    </ul>
  </nav>
  <div class="controls">
    <button class="theme-btn" data-theme="light">Светлая</button>
    <button class="theme-btn" data-theme="dark">Тёмная</button>
    <button class="theme-btn" data-theme="green">Природа</button>
    <button class="theme-btn" data-theme="field">Поле</button>
    <button id="qr-btn" class="theme-btn">QR</button>
  </div>
</header>

<main class="container">
  <!-- MAP -->
  <section id="map-section">
    <h2>Интерактивная карта</h2>
    <div id="map"></div>
    <div id="weather">Нажмите на карту — сервер покажет погоду в точке клика.</div>
  </section>

  <!-- TEAM -->
  <section id="team">
    <h2>Наша команда</h2>
    <div class="train">
      <div class="wagon"><img src="https://via.placeholder.com/300x200" alt=""><p><b>Сагындык</b><br>Бот-разработчик</p></div>
      <div class="wagon"><img src="https://via.placeholder.com/300x200" alt=""><p><b>Камила</b><br>Контент-дизайнер</p></div>
      <div class="wagon"><img src="https://via.placeholder.com/300x200" alt=""><p><b>Ажар</b><br>Ресёрчер</p></div>
      <div class="wagon"><img src="https://via.placeholder.com/300x200" alt=""><p><b>Медина</b><br>SMM</p></div>
      <div class="wagon"><img src="https://via.placeholder.com/300x200" alt=""><p><b>Мирас</b><br>Сайт-разработчик</p></div>
    </div>
  </section>

  <!-- ABOUT -->
  <section id="about">
    <h2>О проекте Egos</h2>
    <p>Egos — умный агроассистент, собирает данные, строит прогнозы и помогает фермерам выбрать лучшее время для работ.</p>
  </section>

  <!-- CHANNELS -->
  <section id="channels">
    <h2>Каналы</h2>
    <p><a id="tg-link" href="https://t.me/Kyzylegis_bot" target="_blank">Наш Telegram</a> — сканируй QR на мобильном.</p>
  </section>
</main>

<footer><p>© 2025 Команда Egos</p></footer>

<!-- Chat widget -->
<button class="chat-toggle" id="chatToggle">💬 Помощник</button>
<div class="chat-window" id="chatWindow" style="display:none">
  <div class="chat-header"><div>Ассистент Egos</div><button id="closeChat">✖</button></div>
  <div class="chat-body" id="chatBody"><div class="msg bot">Привет! Я помогу с полями, погодой и советами по урожаю.</div></div>
  <div class="chat-input">
    <input id="chatInput" placeholder="Напиши вопрос..." />
    <button id="sendBtn">Отправить</button>
  </div>
</div>

<!-- QR modal -->
<div id="qrModal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);align-items:center;justify-content:center;z-index:3000">
  <div style="background:var(--card);padding:18px;border-radius:12px;max-width:90%;text-align:center">
    <h3>Сканируй QR</h3>
    <img id="qrImg" src="" alt="QR" style="width:220px;height:220px">
    <p><a id="qrLink" href="https://bekisevmiras5-web.github.io/egos/" target="_blank">Открыть сайт</a></p>
    <button onclick="document.getElementById('qrModal').style.display='none'">Закрыть</button>
  </div>
</div>

<!-- background music -->
<audio controls autoplay loop style="position:fixed;bottom:10px;left:10px;z-index:2000">
  <source src="https://cdn.pixabay.com/download/audio/2022/10/12/audio_70d8bfa8d4.mp3" type="audio/mp3">
</audio>

<script>
/* ===== THEME SWITCH ===== */
document.querySelectorAll('.theme-btn').forEach(btn=>{
  btn.addEventListener('click', ()=> {
    const t = btn.getAttribute('data-theme');
    if(t==='light') document.body.setAttribute('data-theme','');
    else document.body.setAttribute('data-theme', t);
  });
});

/* ===== MAP & WEATHER ===== */
const map = L.map('map').setView([48, 66], 4);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18}).addTo(map);
map.on('click', async (e) => {
  const lat = e.latlng.lat, lon = e.latlng.lng;
  document.getElementById('weather').textContent = 'Загрузка погоды...';
  try {
    const res = await fetch(`/api/weather?lat=${lat}&lon=${lon}`);
    if(!res.ok) throw new Error('Ошибка сервера');
    const data = await res.json();
    document.getElementById('weather').innerHTML = `
      <h3>Погода: ${data.name || 'неизвестно'}</h3>
      <p>Температура: ${data.temp} °C</p>
      <p>${data.desc}</p>
    `;
  } catch (err) {
    document.getElementById('weather').textContent = 'Не удалось получить погоду.';
    console.error(err);
  }
});

/* ===== CHAT WIDGET ===== */
const chatToggle = document.getElementById('chatToggle');
const chatWindow = document.getElementById('chatWindow');
const closeChat = document.getElementById('closeChat');
const chatBody = document.getElementById('chatBody');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

function appendMsg(text, cls='bot'){
  const d = document.createElement('div');
  d.className = 'msg '+cls;
  d.textContent = text;
  chatBody.appendChild(d);
  chatBody.scrollTop = chatBody.scrollHeight;
}

chatToggle.addEventListener('click', ()=> chatWindow.style.display='flex');
closeChat.addEventListener('click', ()=> chatWindow.style.display='none');

async function sendMessage(){
  const text = chatInput.value.trim();
  if(!text) return;
  appendMsg(text,'user');
  chatInput.value = '';
  appendMsg('Пишу...', 'bot');
  try {
    const res = await fetch('/api/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message:text})
    });
    const data = await res.json();
    const nodes = chatBody.querySelectorAll('.msg.bot');
    if(nodes.length) nodes[nodes.length-1].remove();
    appendMsg(data.reply,'bot');
  } catch (err) {
    const nodes = chatBody.querySelectorAll('.msg.bot');
    if(nodes.length) nodes[nodes.length-1].remove();
    appendMsg('Ошибка: не удалось получить ответ от сервера.', 'bot');
    console.error(err);
  }
}
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keydown', (e)=> { if(e.key==='Enter') sendMessage(); });

/* ===== QR ===== */
document.getElementById('qr-btn').addEventListener('click', async ()=>{
  try {
    const res = await fetch('/api/qr?url='+encodeURIComponent(location.href));
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    document.getElementById('qrImg').src = url;
    document.getElementById('qrLink').href = location.href;
    document.getElementById('qrModal').style.display='flex';
  } catch (err) { alert('Не удалось получить QR'); console.error(err); }
});

document.getElementById('qrModal').addEventListener('click', (e)=>{
  if(e.target.id==='qrModal') e.target.style.display='none';
});
</script>
</body>
</html>
