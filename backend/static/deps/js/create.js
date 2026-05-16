document.addEventListener("DOMContentLoaded", function () {
  const choicesList = document.getElementById("choices-list");
  const addBtn = document.getElementById("add-choice-btn");
  const counterDisplay = document.getElementById("choice-counter");
  const MAX_CHOICES = 20;
  function updateCounter() {
    const count = choicesList.children.length;
    counterDisplay.textContent = `${count} / ${MAX_CHOICES}`;
    addBtn.style.display = count >= MAX_CHOICES ? "none" : "flex";
  }
  addBtn.addEventListener("click", function () {
    const count = choicesList.children.length;
    if (count < MAX_CHOICES) {
      const newChoice = document.createElement("div");
      newChoice.className = "choice-item";
      newChoice.innerHTML = `
                <input required type="text" name="choices" class="form-input" placeholder="Choice ${count + 1}">
                <button type="button" class="btn-remove-choice">✕</button>
            `;
      choicesList.appendChild(newChoice);
      updateCounter();
      newChoice
        .querySelector(".btn-remove-choice")
        .addEventListener("click", function () {
          newChoice.remove();
          updateCounter();
          Array.from(choicesList.children).forEach((item, index) => {
            item.querySelector("input").placeholder = `Choice ${index + 1}`;
          });
        });
    }
  });
});
