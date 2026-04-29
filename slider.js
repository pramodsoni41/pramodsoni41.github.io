function initSlider() {
  const slider = document.querySelector(".slider");
  if (!slider) return;

  const slides = Array.from(
    slider.querySelectorAll(".slide")
  );

  const prevBtn = slider.querySelector(".prev");
  const nextBtn = slider.querySelector(".next");
  const dotsWrap = slider.querySelector(".dots");

  if (!slides.length) return;

  let i = 0;

  /* Create dots dynamically */
  dotsWrap.innerHTML = "";

  slides.forEach((_, idx) => {
    const dot = document.createElement("button");
    dot.className = "dot";
    if (idx === 0) dot.classList.add("active");

    dot.addEventListener("click", () => {
      show(idx);
    });

    dotsWrap.appendChild(dot);
  });

  const dots = Array.from(
    dotsWrap.querySelectorAll(".dot")
  );

  function show(idx) {
    slides[i].classList.remove("active");
    dots[i]?.classList.remove("active");

    i = (idx + slides.length) % slides.length;

    slides[i].classList.add("active");
    dots[i]?.classList.add("active");
  }

  prevBtn?.addEventListener("click", () => show(i - 1));
  nextBtn?.addEventListener("click", () => show(i + 1));

  const autoplay =
    slider.dataset.autoplay === "true";

  const interval = parseInt(
    slider.dataset.interval || "3500",
    10
  );

  let timer = null;

  function start() {
    if (!autoplay || slides.length <= 1) return;

    stop();

    timer = setInterval(() => {
      show(i + 1);
    }, interval);
  }

  function stop() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  slider.addEventListener("mouseenter", stop);
  slider.addEventListener("mouseleave", start);

  start();
}