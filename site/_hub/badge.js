// Marks a draft page as a preview and links to the compare page.
// Hidden when the page is shown inside the compare page itself.
(function () {
  var script = document.currentScript;
  if (!script || window.top !== window.self) return;
  var slug = script.getAttribute("data-design");
  var base = script.getAttribute("data-base") || "";
  var path = location.pathname.slice(base.length) || "/";

  var badge = document.createElement("a");
  badge.href = "/compare/?b=" + encodeURIComponent(slug) + "&path=" + encodeURIComponent(path);
  badge.textContent = "Draft preview \u00b7 compare and give feedback";
  badge.setAttribute("style", [
    "position:fixed", "right:12px", "bottom:12px", "z-index:2147483647",
    "padding:6px 12px", "border-radius:999px", "background:#1b1d22", "color:#fbfaf7",
    "font:500 13px/1.3 -apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif",
    "text-decoration:none", "box-shadow:0 2px 8px rgba(0,0,0,.2)", "max-width:calc(100vw - 24px)"
  ].join(";"));
  document.body.appendChild(badge);
})();
