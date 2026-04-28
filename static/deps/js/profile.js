document.addEventListener("DOMContentLoaded", () => {
  const editBtn = document.getElementById("edit-profile-btn");
  const cancelBtn = document.getElementById("cancel-edit-btn");
  const viewElements = document.querySelectorAll(".view-mode");
  const editElements = document.querySelectorAll(".edit-mode");

  if (editBtn) {
    editBtn.addEventListener("click", () => {
      viewElements.forEach((el) => (el.style.display = "none"));
      editElements.forEach((el) => (el.style.display = "block"));
    });
  }

  if (cancelBtn) {
    cancelBtn.addEventListener("click", () => {
      viewElements.forEach((el) => (el.style.display = "inline-flex"));
      editElements.forEach((el) => (el.style.display = "none"));
    });
  }
});
