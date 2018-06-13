document.body.appendChild(renderer.view);

const wards = {};
const lines = [];

const inpatientsText = new PIXI.Text('');
inpatientsText.x = 200;
inpatientsText.y = 350;
inpatientsText.style = {
  fontFamily: 'Arial',
  fontSize: 24,
  fill: 0x3d1266,
  align: 'center',
};

let frames = 600;
const ticker = new PIXI.ticker.Ticker();
ticker.add((deltaTime) => {
  if (frames < 600) {
    frames += deltaTime;
    renderer.render(stage);
  } else {
    frames = 0;
    lines.forEach(l => stage.removeChild(l));

    fetch('http://127.0.0.1:5000/api/movements')
      .then(response => response.json())
      .then((movements) => {
        Object.keys(movements).forEach((m) => {
          const fromX = wards[m.charAt(0)].children[0].x + 80;
          const fromY = wards[m.charAt(0)].children[0].y + 32;
          const toX = wards[m.charAt(1)].children[0].x + 80;
          const toY = wards[m.charAt(1)].children[0].y + 32;

          const curve = new PIXI.Graphics();
          curve.lineStyle(movements[m], 0x000001);
          curve.moveTo(fromX, fromY);
          curve.bezierCurveTo(280, 137, 280, 237, toX, toY);
          lines.push(curve);
          stage.addChild(curve);
        });
      });

    fetch('http://127.0.0.1:5000/api/data')
      .then(response => response.json())
      .then((status) => {
        Object.keys(status).forEach((bed) => {
          const sprite = wards[Math.floor(((bed - 1) / 5) + 1)].children[(bed - 1) % 5];

          if (status[bed] === 0) {
            sprite.beginFill(0x00FF00);
            sprite.drawRect(0, 0, 32, 64);
          } else if (status[bed].lateDischarge === true) {
            sprite.beginFill(0x551A8B);
            sprite.drawRect(0, 0, 32, 64);
          } else if (status[bed].potentialLateDischarge === true) {
            sprite.beginFill(0xFFA500);
            sprite.drawRect(0, 0, 32, 64);
          } else {
            sprite.beginFill(0xFF0000);
            sprite.drawRect(0, 0, 32, 64);
          }
        });

        const inpatients = Object.values(status).filter(p => p !== 0).length;
        inpatientsText.setText(`Inpatients: ${inpatients}/30`);
      });

    renderer.render(stage);
  }
});


function setup() {
  renderer.backgroundColor = 0xF5F5F5;
  renderer.view.style.position = 'absolute';
  renderer.view.style.display = 'block';
  renderer.autoResize = true;
  renderer.resize(window.innerWidth, window.innerHeight);

  for (let i = 0; i < 6; i += 1) {
    const x = 50 + (300 * (Math.floor((i / 3))));
    const y = (50 + (100 * i)) - (300 * (Math.floor(i / 3)));
    wards[i + 1] = createWard(x, y);
  }

  Object.values(wards).forEach(ward => stage.addChild(ward));

  stage.addChild(infoBox());
  stage.addChild(inpatientsText);

  renderer.render(stage);
  ticker.start();
}

PIXI.loader
  .add([
    'static/img/phtwo.jpg',
  ])
  .load(setup);
