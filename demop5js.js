let jsonData;

function preload() {
  jsonData = loadJSON('https://raw.githubusercontent.com/glyn63/chmov/main/chmov2025jul_u5d48x.json');
}

function setup() {
  createCanvas(400, 300);
  background(220);
  textSize(14);
  fill(0);

  if (jsonData && jsonData.moves) {
    let moveCount = jsonData.moves.length;
    text(`Total moves loaded: ${moveCount}`, 10, 30);

    let firstMove = jsonData.moves[0];
    if (firstMove) {
      text("First move details:", 10, 60);

      let y = 80;
      for (let key in firstMove) {
        let val = firstMove[key];
        if (typeof val === 'object') val = JSON.stringify(val);
        text(`${key}: ${val}`, 10, y, width - 20);
        y += 20;
        if (y > height - 20) break;
      }
    }

    // Log all moves to console
    console.log("All moves details:");
    jsonData.moves.forEach((move, idx) => {
      console.log(`Move #${idx + 1}:`);
      for (const [key, val] of Object.entries(move)) {
        if (typeof val === 'object') {
          console.log(`  ${key}: ${JSON.stringify(val)}`);
        } else {
          console.log(`  ${key}: ${val}`);
        }
      }
    });

  } else {
    fill(255, 0, 0);
    text("Failed to load or parse JSON", 10, 30);
  }
}

function draw() {
  noLoop();
}
