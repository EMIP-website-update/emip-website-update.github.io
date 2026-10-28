// emipws.org: menu toggle on small screens and the Fig. 1 scanpath playback.
(function () {
  "use strict";

  // Menu
  var toggle = document.querySelector(".masthead__toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
  }

  // Year list on workshop pages: folds behind a button on small screens.
  var yearToggle = document.querySelector(".year-toggle");
  var yearList = document.getElementById("year-list");
  if (yearToggle && yearList) {
    yearToggle.addEventListener("click", function () {
      var open = yearToggle.getAttribute("aria-expanded") === "true";
      yearToggle.setAttribute("aria-expanded", String(!open));
      yearList.classList.toggle("is-open", !open);
    });
  }

  // Scanpath: replays the recorded fixations in real time once the figure is on screen.
  var fig = document.querySelector("[data-scanpath]");
  if (!fig) return;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) return;

  var replay = fig.querySelector(".scanpath__replay");
  var steps = fig.querySelectorAll(".scanpath__fixations g");
  var last = steps[steps.length - 1];
  var lastT = last ? parseInt(last.style.getPropertyValue("--t"), 10) || 0 : 0;
  var timer;

  function play() {
    fig.classList.remove("is-playing");
    void fig.getBoundingClientRect(); // restart CSS animations
    fig.classList.add("is-playing");
    if (replay) replay.hidden = true;
    clearTimeout(timer);
    timer = setTimeout(function () {
      if (replay) replay.hidden = false;
    }, lastT + 1000);
  }

  fig.classList.add("is-armed");
  var io = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) {
      io.disconnect();
      play();
    }
  }, { threshold: 0.4 });
  io.observe(fig);

  if (replay) replay.addEventListener("click", play);
})();
