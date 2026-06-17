// =========================
// PROFILE IMAGE ROTATION
// =========================

const profileImages = [
    "assets/images/profile.jpg",
    "assets/images/profile1.jpg",
    "assets/images/profile2.jpg",
    "assets/images/profile3.jpg",
    "assets/images/profile4.jpg",
    "assets/images/profile5.jpg"
];

const profilePhoto =
document.getElementById("profile-photo");

if(profilePhoto){

    let currentProfile = 0;

    setInterval(() => {

        currentProfile =
        (currentProfile + 1)
        % profileImages.length;

        profilePhoto.src =
        profileImages[currentProfile];

    }, 3000);

}


// =========================
// SKILL CAROUSEL
// =========================

const slides =
document.querySelectorAll(".skill-slide");

let current = 0;

function updateCarousel(){

    slides.forEach((slide,index)=>{

        let offset =
        index - current;

        const half =
        Math.floor(slides.length / 2);

        if(offset < -half)
            offset += slides.length;

        if(offset > half)
            offset -= slides.length;

        slide.style.transition =
        "all .6s ease";

        // CENTER

        if(offset === 0){

            slide.style.transform = `
                translate(-50%,-50%)
                translateX(0px)
                scale(1)
                rotateY(0deg)
            `;

            slide.style.zIndex = "10";
            slide.style.opacity = "1";
        }

        // LEFT

        else if(offset === -1){

            slide.style.transform = `
                translate(-50%,-50%)
                translateX(-320px)
                rotateY(40deg)
                scale(.82)
            `;

            slide.style.zIndex = "6";
            slide.style.opacity = ".85";
        }

        // RIGHT

        else if(offset === 1){

            slide.style.transform = `
                translate(-50%,-50%)
                translateX(320px)
                rotateY(-40deg)
                scale(.82)
            `;

            slide.style.zIndex = "6";
            slide.style.opacity = ".85";
        }

        // FAR LEFT

        else if(offset === -2){

            slide.style.transform = `
                translate(-50%,-50%)
                translateX(-600px)
                rotateY(55deg)
                scale(.65)
            `;

            slide.style.zIndex = "2";
            slide.style.opacity = ".45";
        }

        // FAR RIGHT

        else if(offset === 2){

            slide.style.transform = `
                translate(-50%,-50%)
                translateX(600px)
                rotateY(-55deg)
                scale(.65)
            `;

            slide.style.zIndex = "2";
            slide.style.opacity = ".45";
        }

        // HIDDEN

        else{

            slide.style.transform = `
                translate(-50%,-50%)
                translateX(${offset * 900}px)
                scale(.4)
            `;

            slide.style.zIndex = "0";
            slide.style.opacity = "0";
        }

    });

}


// =========================
// BUTTONS
// =========================

const nextBtn =
document.getElementById("nextSkill");

const prevBtn =
document.getElementById("prevSkill");

if(nextBtn && prevBtn && slides.length){

    nextBtn.addEventListener("click",()=>{

        current =
        (current + 1)
        % slides.length;

        updateCarousel();
    });

    prevBtn.addEventListener("click",()=>{

        current =
        (current - 1 + slides.length)
        % slides.length;

        updateCarousel();
    });

    updateCarousel();
}

const timelineSlides =
document.querySelectorAll(".timeline-slide");

let timelineCurrent = 0;

function updateTimeline(){

    timelineSlides.forEach((slide,index)=>{

        let offset =
        index - timelineCurrent;

        if(offset < -7)
            offset += timelineSlides.length;

        if(offset > 7)
            offset -= timelineSlides.length;

        if(offset === 0){

            slide.style.transform =
            `
            translate(-50%,-50%)
            translateY(0px)
            scale(1)
            `;

            slide.style.opacity = 1;
            slide.style.zIndex = 10;
        }

        else if(offset === -1){

            slide.style.transform =
            `
            translate(-50%,-50%)
            translateY(-180px)
            scale(.8)
            `;

            slide.style.opacity = .5;
            slide.style.zIndex = 5;
        }

        else if(offset === 1){

            slide.style.transform =
            `
            translate(-50%,-50%)
            translateY(180px)
            scale(.8)
            `;

            slide.style.opacity = .5;
            slide.style.zIndex = 5;
        }

        else{

            slide.style.opacity = 0;
            slide.style.zIndex = 0;

            slide.style.transform =
            `
            translate(-50%,-50%)
            translateY(${offset*400}px)
            scale(.5)
            `;
        }

    });

}

document
.getElementById("nextTimeline")
.addEventListener("click",()=>{

    timelineCurrent =
    (timelineCurrent+1)
    % timelineSlides.length;

    updateTimeline();
});

document
.getElementById("prevTimeline")
.addEventListener("click",()=>{

    timelineCurrent =
    (timelineCurrent-1+timelineSlides.length)
    % timelineSlides.length;

    updateTimeline();
});





function createSimpleSlider(
    slideClass,
    prevBtn,
    nextBtn
){

    const slides =
    document.querySelectorAll(slideClass);

    let current = 0;

    function update(){

        slides.forEach((slide,index)=>{

            if(index === current){

                slide.style.opacity = 1;
                slide.style.transform =
                "translateY(0px)";

                slide.style.zIndex = 10;
            }

            else{

                slide.style.opacity = 0;

                slide.style.transform =
                "translateY(40px)";

                slide.style.zIndex = 0;
            }

        });

    }

    document
    .getElementById(prevBtn)
    .addEventListener("click",()=>{

        current =
        (current-1+slides.length)
        %slides.length;

        update();

    });

    document
    .getElementById(nextBtn)
    .addEventListener("click",()=>{

        current =
        (current+1)
        %slides.length;

        update();

    });

    update();
}

function getAllProjects() {

    const allProjects = [];

    categories.forEach(category => {

        category.projects.forEach(project => {

            allProjects.push({
                ...project,
                category: category.name
            });

        });

    });

    return allProjects;
}

function getRandomProjects(count = 3) {

    const projects =
    [...getAllProjects()];

    for(
        let i = projects.length - 1;
        i > 0;
        i--
    ){

        const j =
        Math.floor(
            Math.random() * (i + 1)
        );

        [projects[i], projects[j]] =
        [projects[j], projects[i]];
    }

    return projects.slice(0, count);
}

function loadFeaturedProjects() {

    const container =
    document.getElementById(
        "featuredProjects"
    );

    if(!container) return;

    const featured =
    getRandomProjects(3);

	container.innerHTML =
	featured.map(project => `

		<div class="project-slide">

			<img
				src="assets/images/projects/${project.image}"
				alt="${project.title}"
				class="featured-project-image"
			>

			<h3 class="featured-project-title">
				${project.title}
			</h3>

		</div>

	`).join("");
}

updateTimeline();

loadFeaturedProjects();

createSimpleSlider(
    ".project-slide",
    "prevProject",
    "nextProject"
);

createSimpleSlider(
    ".blog-slide",
    "prevBlog",
    "nextBlog"
);