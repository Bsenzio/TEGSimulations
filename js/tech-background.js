// =====================================================
// BCI / EEG / Neural Network Background
// Bruno Senzio-Savino Website
// =====================================================

const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");

canvas.id = "tech-background";

canvas.style.position = "fixed";
canvas.style.top = "0";
canvas.style.left = "0";
canvas.style.width = "100%";
canvas.style.height = "100%";
canvas.style.zIndex = "0";
canvas.style.pointerEvents = "none";

document.body.prepend(canvas);

// =====================================================
// RESIZE
// =====================================================

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

resizeCanvas();
window.addEventListener("resize", resizeCanvas);

// =====================================================
// NEURAL NETWORK NODES
// =====================================================

const nodes = [];

for (let i = 0; i < 70; i++) {
    nodes.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4
    });
}

// =====================================================
// EEG SIGNALS
// =====================================================

const eegLines = [];

for (let i = 0; i < 12; i++) {
    eegLines.push({
        y: i * 120 + 50,
        phase: Math.random() * 10
    });
}

function drawEEG(){

    eegLines.forEach(line=>{

        ctx.beginPath();

        ctx.strokeStyle =
        "rgba(0,255,255,0.35)";

        ctx.lineWidth = 2;

        let y = line.y;

        for(let x=0;x<canvas.width;x+=8){

            let signal =
            Math.sin(
                x*0.015 +
                Date.now()*0.002 +
                line.phase
            )*8;

            if(Math.random()<0.02){

                signal -= 35;
                signal += 60;
                signal -= 25;
            }

            const yy = y + signal;

            if(x===0)
                ctx.moveTo(x,yy);
            else
                ctx.lineTo(x,yy);
        }

        ctx.stroke();
    });
}

// =====================================================
// CIRCUIT GRID
// =====================================================

function drawCircuits() {

    ctx.strokeStyle = "rgba(0,255,150,0.12)";
    ctx.lineWidth = 1;

    for (let x = 0; x < canvas.width; x += 140) {

        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }

    for (let y = 0; y < canvas.height; y += 140) {

        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
}

// =====================================================
// NEURAL NETWORK
// =====================================================

function drawNetwork() {

    nodes.forEach(node => {

        node.x += node.vx;
        node.y += node.vy;

        if (node.x < 0 || node.x > canvas.width)
            node.vx *= -1;

        if (node.y < 0 || node.y > canvas.height)
            node.vy *= -1;

        ctx.beginPath();
        ctx.arc(node.x, node.y, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = "#00ffff";
        ctx.fill();
    });

    for (let i = 0; i < nodes.length; i++) {

        for (let j = i + 1; j < nodes.length; j++) {

            const dx = nodes[i].x - nodes[j].x;
            const dy = nodes[i].y - nodes[j].y;

            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 140) {

                ctx.strokeStyle =
                    `rgba(0,255,255,${0.7 - dist / 200})`;

                ctx.lineWidth = 0.6;

                ctx.beginPath();
                ctx.moveTo(nodes[i].x, nodes[i].y);
                ctx.lineTo(nodes[j].x, nodes[j].y);
                ctx.stroke();
            }
        }
    }
}

// =====================================================
// DIGITAL BRAINS
// =====================================================

const brains = [];

for (let i = 0; i < 5; i++) {

    brains.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        size: 40 + Math.random() * 30,
        phase: Math.random() * 10
    });
}

function drawBrains(){

    brains.forEach(b=>{

        b.x += 0.25;

        if(b.x > canvas.width + 120){

            b.x = -120;
            b.y = Math.random()*canvas.height;
        }

        const pulse =
        Math.sin(
            Date.now()*0.002+b.phase
        )*3;

        ctx.strokeStyle =
        "rgba(255,0,255,0.45)";

        ctx.lineWidth = 2;

        // hemisferios

        ctx.beginPath();
        ctx.arc(
            b.x-18,
            b.y,
            25+pulse,
            0,
            Math.PI*2
        );
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(
            b.x+18,
            b.y,
            25+pulse,
            0,
            Math.PI*2
        );
        ctx.stroke();

        // surcos

        for(let i=-15;i<=15;i+=8){

            ctx.beginPath();

            ctx.moveTo(
                b.x-10,
                b.y+i
            );

            ctx.lineTo(
                b.x+10,
                b.y+i
            );

            ctx.stroke();
        }
    });
}

// =====================================================
// SYNAPSES
// =====================================================

const synapses = [];
const spikes = [];

for (let i = 0; i < 45; i++) {

    synapses.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5
    });
}

function drawSynapses() {

    synapses.forEach(s => {

        s.x += s.vx;
        s.y += s.vy;

        if (s.x < 0) s.x = canvas.width;
        if (s.x > canvas.width) s.x = 0;

        if (s.y < 0) s.y = canvas.height;
        if (s.y > canvas.height) s.y = 0;

        ctx.fillStyle = "rgba(255,255,0,0.9)";

        ctx.beginPath();
        ctx.arc(s.x,s.y,3,0,Math.PI*2);
        ctx.fill();
		
		if(Math.random()<0.002){

			spikes.push({

				x:s.x,
				y:s.y,
				radius:2,
				life:1
			});
		}		
		
    });

    for (let i = 0; i < synapses.length; i++) {

        for (let j = i + 1; j < synapses.length; j++) {

            const dx =
                synapses[i].x - synapses[j].x;

            const dy =
                synapses[i].y - synapses[j].y;

            const d =
                Math.sqrt(dx * dx + dy * dy);

            if (d < 100) {

                ctx.strokeStyle =
                    `rgba(255,0,255,${
                        0.4 - d / 250
                    })`;

                ctx.lineWidth = 0.5;

                ctx.beginPath();
                ctx.moveTo(
                    synapses[i].x,
                    synapses[i].y
                );
                ctx.lineTo(
                    synapses[j].x,
                    synapses[j].y
                );
                ctx.stroke();
            }
        }
    }
}


function drawSpikes(){

    for(let i=spikes.length-1;i>=0;i--){

        const sp = spikes[i];

        sp.radius += 1.5;

        sp.life -= 0.02;

        ctx.strokeStyle =
        `rgba(255,255,0,${sp.life})`;

        ctx.lineWidth = 2;

        ctx.beginPath();

        ctx.arc(
            sp.x,
            sp.y,
            sp.radius,
            0,
            Math.PI*2
        );

        ctx.stroke();

        if(sp.life<=0){

            spikes.splice(i,1);
        }
    }
}



// =====================================================
// SCANNER
// =====================================================

function drawScanner() {

    const y =
        (Date.now() * 0.05) %
        canvas.height;

    ctx.strokeStyle =
        "rgba(0,255,255,0.15)";

    ctx.lineWidth = 2;

    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
}

const pixels=[];

for(let i=0;i<40;i++){

    pixels.push({

        x:Math.random()*window.innerWidth,
        y:Math.random()*window.innerHeight,

        speed:1+Math.random()*2,

        size:4+Math.random()*6
    });
}

function drawRetroPixels(){

    pixels.forEach(p=>{

        p.y += p.speed;

        if(p.y > canvas.height){

            p.y = -20;
            p.x = Math.random()*canvas.width;
        }

        ctx.fillStyle =
        "rgba(255,255,255,0.25)";

        ctx.fillRect(
            p.x,
            p.y,
            p.size,
            p.size
        );
    });
}


const gameIcons = [];

const symbols = [
    "▲",
    "■",
    "◆",
    "●",
    "✦"
];

for(let i=0;i<20;i++){

    gameIcons.push({

        x:Math.random()*window.innerWidth,
        y:Math.random()*window.innerHeight,

        speed:0.3+Math.random()*0.5,

        symbol:
        symbols[
            Math.floor(
                Math.random()*symbols.length
            )
        ]
    });
}

function drawGameIcons(){

    ctx.font =
    "18px 'Orbitron', sans-serif";

    gameIcons.forEach(g=>{

        g.y += g.speed;

        if(g.y > canvas.height){

            g.y = -20;
            g.x =
            Math.random()*canvas.width;
        }

        ctx.fillStyle =
        "rgba(255,255,255,0.25)";

        ctx.fillText(
            g.symbol,
            g.x,
            g.y
        );
    });
}

function drawHeroBrain(){

    const x = canvas.width/2;
    const y = 220;

    ctx.strokeStyle =
    "rgba(0,255,255,0.03)";

    ctx.lineWidth = 6;

    ctx.beginPath();
    ctx.arc(x-90,y,130,0,Math.PI*2);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(x+90,y,130,0,Math.PI*2);
    ctx.stroke();

    for(let i=-90;i<=90;i+=20){

        ctx.beginPath();

        ctx.moveTo(
            x-40,
            y+i
        );

        ctx.lineTo(
            x+40,
            y+i
        );

        ctx.stroke();
    }
}


// =====================================================
// ANIMATION LOOP
// =====================================================
function animateBackground(){

    ctx.fillStyle =
    "rgba(5,11,22,0.15)";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawHeroBrain();
    drawCircuits();
    drawEEG();
    drawNetwork();
    drawBrains();
    drawSynapses();
    drawSpikes();
    drawGameIcons();
    drawRetroPixels();
    drawScanner();

    requestAnimationFrame(
        animateBackground
    );
}
animateBackground();