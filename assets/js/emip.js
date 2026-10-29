// emipws.org: menu, one-page section jumps, year list toggle and the scanpath over the venue photo.
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

  // One-page homepage: close the phone menu once a section is picked, then jump,
  // so the distance isn't measured while the open menu still pushes the page down.
  if (toggle && nav) {
    nav.addEventListener("click", function (e) {
      var link = e.target.closest("a");
      if (!link || !nav.classList.contains("is-open")) return;
      toggle.setAttribute("aria-expanded", "false");
      nav.classList.remove("is-open");
      var url = new URL(link.href);
      var section = url.pathname === location.pathname && url.hash && document.getElementById(url.hash.slice(1));
      if (section) {
        e.preventDefault();
        history.pushState(null, "", url.hash);
        section.scrollIntoView();
      }
    });
  }

  // Mark the menu item of the section being read (the intro clears it).
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

  // Venue photo: replays the illustrative scanpath once the photo is on screen.
  var gaze = document.querySelector("[data-gaze]");
  var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (gaze && !still && "IntersectionObserver" in window) {
    var replay = gaze.querySelector(".gaze__replay");
    var dots = gaze.querySelectorAll(".gaze__fixations g");
    var lastT = dots.length ? parseInt(dots[dots.length - 1].style.getPropertyValue("--t"), 10) || 0 : 0;
    var timer;
    var play = function () {
      gaze.classList.remove("is-playing");
      void gaze.getBoundingClientRect(); // restart CSS animations
      gaze.classList.add("is-playing");
      if (replay) replay.hidden = true;
      clearTimeout(timer);
      timer = setTimeout(function () { if (replay) replay.hidden = false; }, lastT + 1000);
    };
    gaze.classList.add("is-armed");
    var seen = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        seen.disconnect();
        play();
      }
    }, { threshold: 0.4 });
    seen.observe(gaze);
    if (replay) replay.addEventListener("click", play);
  }
})();
