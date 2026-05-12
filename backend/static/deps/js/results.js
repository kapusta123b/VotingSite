document.addEventListener("DOMContentLoaded", () => {
  const fills = document.querySelectorAll(".progress-fill");
  setTimeout(() => {
    fills.forEach((fill) => {
      fill.style.width = fill.getAttribute("data-width");
    });
  }, 100);
});
