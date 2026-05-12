document.addEventListener("DOMContentLoaded", () => {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll("nav ul li a");
  navLinks.forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });
  const copyButtons = document.querySelectorAll(".btn-outline");
  copyButtons.forEach((btn) => {
    if (btn.textContent.trim() === "Copy Link") {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        navigator.clipboard.writeText(window.location.href).then(() => {
          const originalText = btn.textContent;
          btn.textContent = "Copied!";
          btn.style.color = "var(--success)";
          setTimeout(() => {
            btn.textContent = originalText;
            btn.style.color = "";
          }, 2000);
        });
      });
    }
  });

  const cards = document.querySelectorAll(".card");

  cards.forEach((card) => {
    const deleteBtn = card.querySelector(".delete-btn-trigger");
    const overlay = card.querySelector(".delete-confirmation-overlay");
    const cancelBtn = card.querySelector(".btn-cancel");
    const confirmInput = card.querySelector(".confirm-input");
    const confirmDeleteBtn = card.querySelector(".btn-delete-confirm");
    const targetText = card.querySelector("strong").textContent.trim();

    if (deleteBtn) {
      deleteBtn.addEventListener("click", () => {
        overlay.classList.add("active");
        confirmInput.focus();
      });
    }

    if (cancelBtn) {
      cancelBtn.addEventListener("click", () => {
        overlay.classList.remove("active");
        confirmInput.value = "";
        confirmDeleteBtn.disabled = true;
      });
    }

    if (confirmInput) {
      confirmInput.addEventListener("input", (e) => {
        if (e.target.value.trim() === targetText) {
          confirmDeleteBtn.disabled = false;
        } else {
          confirmDeleteBtn.disabled = true;
        }
      });
    }

    if (confirmDeleteBtn) {
      confirmDeleteBtn.addEventListener("click", () => {
        console.log("Deleting poll:", targetText);
      });
    }
  });

  // Filter Glider Logic
  const filterForm = document.getElementById("filter-form");
  if (filterForm) {
    const buttons = filterForm.querySelectorAll(".filter-btn");
    const glider = filterForm.querySelector(".filter-glider");
    const activeBtn = filterForm.querySelector(".filter-btn.active");

    const moveGlider = (btn) => {
      if (!btn) return;
      glider.style.width = `${btn.offsetWidth}px`;
      glider.style.left = `${btn.offsetLeft}px`;
    };

    if (activeBtn) {
      setTimeout(() => moveGlider(activeBtn), 50);
    }

    buttons.forEach((btn) => {
      btn.addEventListener("mouseenter", () => moveGlider(btn));
    });

    filterForm.addEventListener("mouseleave", () => {
      moveGlider(activeBtn);
    });
    
    window.addEventListener("resize", () => moveGlider(activeBtn));
  }

  // Auto-dismiss messages
  const messages = document.querySelectorAll(".message-toast");
  messages.forEach((message) => {
    setTimeout(() => {
      message.classList.add("message-fade-out");
      setTimeout(() => {
        message.remove();
      }, 300);
    }, 5000);
  });
});
