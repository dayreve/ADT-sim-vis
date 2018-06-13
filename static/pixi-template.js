const stage = new PIXI.Container();
const renderer = PIXI.autoDetectRenderer(1,1);
const info = new PIXI.Text('');

function infoBox() {
  info.x = 600;
  info.y = 50;
  info.style = {
    fontFamily: 'Arial',
    fontSize: 24,
    fill: 0x4a5b77,
    align: 'center',
  };

  return info;
}

function onPointerOver() {
  const t = this;

  const status = fetch('http://127.0.0.1:5000/api/data')
    .then(response => response.json())
    .then((status) => {
      const bed = (stage.children.indexOf(t.parent) * 5) + t.parent.children.indexOf(t) + 1;
      if (status[bed] === 0) {
        info.setText('unoccupied');
      } else {
        info.setText(`
          Patient number: ${status[bed].patNo}\n
          Patient name: ${status[bed].name}\n
          Patient DOB: ${status[bed].dob}\n
          Patient gender: ${status[bed].gender}\n
          Patient NEWS: ${status[bed].news}\n
          Patient EDD: ${status[bed].edd}
        `);
      }
    });

  return status;
}

function onPointerOut() {
  info.setText('');
}

function onPointerDown() {
}

function onPointerUp() {
}

function createBed(x, y) {
  const rect = new PIXI.Graphics();
  rect.lineStyle(4, 0x918C8C, 1);
  rect.beginFill(0xFFE4E4);
  rect.drawRect(0, 0, 32, 64);
  rect.endFill();
  rect.x = x;
  rect.y = y;
  rect.interactive = true;
  rect.buttonMode = true;

  rect
    .on('pointerover', onPointerOver)
    .on('pointerout', onPointerOut)
    .on('pointerdown', onPointerDown)
    .on('pointerup', onPointerUp);

  return rect;
}

function createWard(x, y) {
  const ward = new PIXI.Container();

  for (let i = 0; i < 5; i += 1) {
    ward.addChild(createBed((i * 32) + x, y));
  }

  return ward;
}
