document.addEventListener("DOMContentLoaded", () => {
  const slider = document.querySelector(".slider");
  if (!slider) return;

  const slides = Array.from(slider.querySelectorAll(".slide"));
  const dots = Array.from(slider.querySelectorAll(".dot"));
  const prevBtn = slider.querySelector(".prev");
  const nextBtn = slider.querySelector(".next");

  let i = slides.findIndex(s => s.classList.contains("active"));
  if (i < 0) i = 0;

  const show = (idx) => {
    slides[i].classList.remove("active");
    dots[i]?.classList.remove("active");
    i = (idx + slides.length) % slides.length;
    slides[i].classList.add("active");
    dots[i]?.classList.add("active");
  };

  prevBtn?.addEventListener("click", () => show(i - 1));
  nextBtn?.addEventListener("click", () => show(i + 1));
  dots.forEach((d, idx) => d.addEventListener("click", () => show(idx)));

  const autoplay = slider.dataset.autoplay === "true";
  const interval = parseInt(slider.dataset.interval || "3500", 10);

  let timer = null;
  const start = () => {
    if (!autoplay || slides.length <= 1) return;
    timer = setInterval(() => show(i + 1), interval);
  };
  const stop = () => { if (timer) clearInterval(timer); timer = null; };

  slider.addEventListener("mouseenter", stop);
  slider.addEventListener("mouseleave", start);
  start();
});
