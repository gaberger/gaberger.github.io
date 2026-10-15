// Click-to-zoom for images in posts. Opens the image full-screen, fitted to the
// window; clicking it again shows it at full resolution so it can be panned.
(function () {
  var selector = ".prose p > img, .prose picture img";
  var overlay, shown, opener;

  function visibleImage(img) {
    // A diagram with light and dark versions has both <img>s; zoom the one on screen.
    var pic = img.closest("picture");
    if (!pic) return img;
    var imgs = pic.querySelectorAll("img");
    for (var i = 0; i < imgs.length; i++) if (imgs[i].offsetParent !== null) return imgs[i];
    return img;
  }

  function close() {
    if (!overlay) return;
    overlay.remove(); overlay = null; shown = null;
    document.documentElement.classList.remove("zoom-open");
    document.removeEventListener("keydown", onKey);
    if (opener) opener.focus();
  }

  function onKey(e) { if (e.key === "Escape") close(); }

  function open(img) {
    img = visibleImage(img);
    opener = img;
    overlay = document.createElement("div");
    overlay.className = "zoom-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", img.alt || "Image");

    var btn = document.createElement("button");
    btn.className = "zoom-close";
    btn.type = "button";
    btn.setAttribute("aria-label", "Close");
    btn.textContent = "×";

    shown = document.createElement("img");
    shown.src = img.currentSrc || img.src;
    shown.alt = img.alt || "";
    shown.title = "Click to view full size";

    var caption = document.createElement("p");
    caption.className = "zoom-caption";
    caption.textContent = img.alt || "";

    overlay.appendChild(btn);
    overlay.appendChild(shown);
    if (img.alt) overlay.appendChild(caption);
    document.body.appendChild(overlay);
    document.documentElement.classList.add("zoom-open");
    document.addEventListener("keydown", onKey);
    btn.focus();

    btn.addEventListener("click", close);
    overlay.addEventListener("click", function (e) { if (e.target === overlay || e.target === caption) close(); });
    shown.addEventListener("click", function (e) {
      e.stopPropagation();
      overlay.classList.toggle("is-full");
      shown.title = overlay.classList.contains("is-full") ? "Click to fit to screen" : "Click to view full size";
    });
  }

  document.querySelectorAll(selector).forEach(function (img) {
    img.classList.add("zoomable");
    img.setAttribute("tabindex", "0");
    img.setAttribute("role", "button");
    img.setAttribute("aria-label", "Enlarge image" + (img.alt ? ": " + img.alt : ""));
    img.addEventListener("click", function () { open(img); });
    img.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(img); }
    });
  });
})();
