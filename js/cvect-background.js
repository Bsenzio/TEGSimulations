const canvas = document.getElementById("cvect-background");
const ctx = canvas.getContext("2d");

let width;
let height;

function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
}

window.addEventListener("resize", resize);
resize();


// ======================================
// SNOW PARTICLES
// ======================================

const snowflakes = [];

for (let i = 0; i < 120; i++) {

    snowflakes.push({
        x: Math.random() * width,
        y: Math.random() * height,
        r: Math.random() * 3 + 1,
        speed: Math.random() * 1 + 0.3
    });

}


// ======================================
// ENERGY PULSES
// ======================================

const pulses = [];

for (let i = 0; i < 20; i++) {

    pulses.push({
        progress: Math.random(),
        speed: 0.002 + Math.random() * 0.003
    });

}


// ======================================
// TEG GRID
// ======================================

function drawGrid() {

    const spacing = 80;

    ctx.strokeStyle = "rgba(120,200,255,0.08)";
    ctx.lineWidth = 1;

    for (let x = 0; x < width; x += spacing) {

        for (let y = 0; y < height; y += spacing) {

            ctx.beginPath();
            ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(150,220,255,0.15)";
            ctx.fill();

            if (x + spacing < width) {

                ctx.beginPath();
                ctx.moveTo(x, y);
                ctx.lineTo(x + spacing, y);
                ctx.stroke();

            }

            if (y + spacing < height) {

                ctx.beginPath();
                ctx.moveTo(x, y);
                ctx.lineTo(x, y + spacing);
                ctx.stroke();

            }
        }
    }
}


// ======================================
// ENERGY FLOW
// ======================================

function drawPulses() {

    const spacing = 80;

    pulses.forEach(p => {

        p.progress += p.speed;

        if (p.progress > 1)
            p.progress = 0;

        const totalLength = width;

        const x = p.progress * totalLength;
        const y = height * 0.7;

        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);

        ctx.fillStyle = "rgba(0,255,180,0.9)";
        ctx.shadowColor = "#00ffb4";
        ctx.shadowBlur = 15;
        ctx.fill();

    });

    ctx.shadowBlur = 0;
}


// ======================================
// SNOW
// ======================================

function drawSnow() {

    ctx.fillStyle = "rgba(255,255,255,0.8)";

    snowflakes.forEach(flake => {

        ctx.beginPath();
        ctx.arc(
            flake.x,
            flake.y,
            flake.r,
            0,
            Math.PI * 2
        );
        ctx.fill();

        flake.y += flake.speed;

        if (flake.y > height) {

            flake.y = -10;
            flake.x = Math.random() * width;

        }

    });

}


// ======================================
// THERMAL GRADIENT
// ======================================

function drawThermalGradient() {

    const gradient = ctx.createLinearGradient(
        0,
        0,
        0,
        height
    );

    gradient.addColorStop(
        0,
        "rgba(0,100,255,0.20)"
    );

    gradient.addColorStop(
        0.5,
        "rgba(0,0,0,0)"
    );

    gradient.addColorStop(
        1,
        "rgba(255,120,0,0.15)"
    );

    ctx.fillStyle = gradient;
    ctx.fillRect(
        0,
        0,
        width,
        height
    );
}


// ======================================
// ANIMATION LOOP
// ======================================

function animate() {

    ctx.clearRect(
        0,
        0,
        width,
        height
    );

    drawThermalGradient();

    drawGrid();

    drawPulses();

    drawSnow();

    requestAnimationFrame(
        animate
    );
}

animate();