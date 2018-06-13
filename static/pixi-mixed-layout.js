document.body.appendChild(renderer.view);

PIXI.loader
    .add([
        "static/img/phtwo.jpg"
    ])
    .load(setup);

function setup() {

    renderer.backgroundColor = 0xF5F5F5;
    renderer.view.style.position = "absolute";
    renderer.view.style.display = "block";
    renderer.autoResize = true;
    renderer.resize(window.innerWidth, window.innerHeight);

    for (let i = 0; i < 6; i++) {
        stage.addChild(createWard(1000, 50 + i * 100));
    }

    renderer.render(stage);
    animationLoop();

}

var t = 100;
function animationLoop() {

    if (t++ < 100) {
        requestAnimationFrame(animationLoop);
        renderer.render(stage);
        return;
    }

    t = 0;
   
    var status = fetch(`http://127.0.0.1:5000/api/data`)
        .then(function(response) {
            return response.json();
        })
        .then(function(status) {
            for (var bed in status) {

                var sprite = stage.children[Math.floor((bed-1)/5)].children[(bed - 1) % 5];
    
                if (status[bed] == 0) {
                    sprite.beginFill(0x00FF00);
                    sprite.drawRect(0,0,32,64);
                }
                else {
                    sprite.beginFill(0xFF0000);
                    sprite.drawRect(0,0,32,64);
                }
            }
        });

    requestAnimationFrame(animationLoop);
    renderer.render(stage);

}
