# lightning tempo
školní projekt hra
<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lightning Tempo</title>
  <style>
    body {
      margin: 0;
      background: #0d0d1a;
      color: #fff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      overflow: hidden;
    }

   
  </style>
</head>
<body>
 h1 {
      margin: 10px;
      font-size: 2.5rem;
      text-shadow: 0 0 15px #00e5ff;
    }

  <h1>⚡ LIGHTNING TEMPO ⚡</h1>
  
  <div class="info-bar">
    <div>Skóre: <span id="score">0</span></div>
    <div>Životy: <span id="lives">3</span></div>
    <div>Tempo: <span id="tempo">1.0x</span></div>
  </div>

  <div class="game-container">
    <div class="lane" id="lane-A"><div class="key-label">A</div></div>
    <div class="lane" id="lane-S"><div class="key-label">S</div></div>
    <div class="lane" id="lane-D"><div class="key-label">D</div></div>
    <div class="lane" id="lane-F"><div class="key-label">F</div></div>
  </div>

  <button id="start-btn" onclick="startGame()">Start Hry</button>

  <script>
    const keys = ['a', 's', 'd', 'f'];
    let activeKey = null;
    let score = 0;
    let lives = 3;
    let speed = 1200; // Počáteční čas na reakci v ms
    let gameTimeout = null;
    let isPlaying = false;

    function startGame() {
      score = 0;
      lives = 3;
      speed = 1200;
      isPlaying = true;
      document.getElementById('score').innerText = score;
      document.getElementById('lives').innerText = lives;
      document.getElementById('tempo').innerText = '1.0x';
      document.getElementById('start-btn').style.display = 'none';
      nextLightning();
    }

    function nextLightning() {
      if (!isPlaying) return;

      // Vyčistit předchozí aktivní dráhu
      if (activeKey) {
        document.getElementById(`lane-${activeKey.toUpperCase()}`).classList.remove('active');
      }

      // Výběr náhodného klávesy
      const randomIndex = Math.floor(Math.random() * keys.length);
      activeKey = keys[randomIndex];

      const lane = document.getElementById(`lane-${activeKey.toUpperCase()}`);
      lane.classList.add('active');

      // Nastavení časovače pro stihnutí reakce
      gameTimeout = setTimeout(() => {
        // Hráč nestihl zareagovat
        lane.classList.remove('active');
        activeKey = null;
        loseLife();
      }, speed);
    }

    document.addEventListener('keydown', (e) => {
      if (!isPlaying || !activeKey) return;

      const pressedKey = e.key.toLowerCase();
      if (keys.includes(pressedKey)) {
        clearTimeout(gameTimeout);
        const lane = document.getElementById(`lane-${activeKey.toUpperCase()}`);
        lane.classList.remove('active');

        if (pressedKey === activeKey) {
          // Správná klávesa
          score += 10;
          document.getElementById('score').innerText = score;
          
          // Zvýšení tempa každých 50 bodů
          if (score % 50 === 0 && speed > 400) {
            speed -= 100;
            const tempoVal = (1200 / speed).toFixed(1);
            document.getElementById('tempo').innerText = `${tempoVal}x`;
          }

          activeKey = null;
          setTimeout(nextLightning, 200);
        } else {
          // Špatná klávesa
          activeKey = null;
          loseLife();
        }
      }
    });

    function loseLife() {
      lives--;
      document.getElementById('lives').innerText = lives;

      if (lives <= 0) {
        gameOver();
      } else {
        setTimeout(nextLightning, 500);
      }
    }

    function gameOver() {
      isPlaying = false;
      alert(`Konec hry! Tvoje finální skóre: ${score}`);
      document.getElementById('start-btn').style.display = 'inline-block';
      document.getElementById('start-btn').innerText = 'Hrát znovu';
    }
  </script>
</body>
</html>
