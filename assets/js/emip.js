// emipws.org: the Menu button on smaller screens, the section marker in the top
// menu, and the Fig. 1 scanpath playback on the homepage.
(function () {
  "use strict";
  var root = document.documentElement;

  // Menu button (below 64rem): opens the side menu as a panel under the header.
  var toggle = document.querySelector(".masthead__toggle");
  var menu = document.getElementById("site-menu");
  var masthead = document.querySelector(".masthead");
  if (toggle && menu && masthead) {
    var setOpen = function (open) {
      root.style.setProperty("--masthead-h", masthead.offsetHeight + "px");
      root.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", String(open));
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && root.classList.contains("menu-open")) {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  // Top menu: mark the homepage section being read (the hero clears it).
  var nav = document.getElementById("site-nav");
  var spied = [];
  var intro = document.querySelector(".event-hero");
  if (intro) spied.push({ link: null, section: intro });
  Array.prototype.forEach.call(nav ? nav.querySelectorAll("a") : [], function (a) {
    var url = new URL(a.href);
    var section = url.pathname === location.pathname && url.hash && document.getElementById(url.hash.slice(1));
    if (section) spied.push({ link: a, section: section });
  });
  if (spied.length > 1 && "IntersectionObserver" in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        spied.forEach(function (s) {
          if (s.link) s.link.classList.toggle("is-current", s.section === entry.target);
        });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    spied.forEach(function (s) { spy.observe(s.section); });
  }

  // Fig. 1: replays the recorded fixations in real time once the figure is on screen.
  var fig = document.querySelector("[data-scanpath]");
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (fig && !still && "IntersectionObserver" in window) {
    var replay = fig.querySelector(".scanpath__replay");
    var steps = fig.querySelectorAll(".scanpath__fixations g");
    var last = steps[steps.length - 1];
    var lastT = last ? parseInt(last.style.getPropertyValue("--t"), 10) || 0 : 0;
    var timer;
    var play = function () {
      fig.classList.remove("is-playing");
      void fig.getBoundingClientRect(); // restart CSS animations
      fig.classList.add("is-playing");
      if (replay) replay.hidden = true;
      clearTimeout(timer);
      timer = setTimeout(function () { if (replay) replay.hidden = false; }, lastT + 1000);
    };
    fig.classList.add("is-armed");
    var seen = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        seen.disconnect();
        play();
      }
    }, { threshold: 0.4 });
    seen.observe(fig);
    if (replay) replay.addEventListener("click", play);
  }
})();
