// Active class
// let all_buttons

// Modal implementation
document.addEventListener("DOMContentLoaded", () => {
  (document.querySelectorAll(".notification .delete") || []).forEach(
    ($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    }
  );

	const menuBtns = document.querySelectorAll(".menu-list .menu-tabs");

	menuBtns.forEach((tab) => {
    tab.addEventListener("click", (e) => {
      menuBtns.forEach((btn) => btn.classList.remove("is-active"));
      e.target.classList.toggle("is-active");
    });
  });

  // Functions to open and close a modal

  function openModal($el) {
    $el.classList.add("is-active");
  }

  function closeModal($el) {
    $el.classList.remove("is-active");
  }

  function closeAllModals() {
    (document.querySelectorAll(".modal") || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll(".js-modal-trigger") || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener("click", () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (
    document.querySelectorAll(
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button"
    ) || []
  ).forEach(($close) => {
    const $target = $close.closest(".modal");

    $close.addEventListener("click", () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener("keydown", (event) => {
    const e = event || window.event;

    if (e.keyCode === 27) {
      // Escape key
      closeAllModals();
    }
  });

  // generate passwords and id
  const generateData = document.getElementById("gen-code");

  generateData.addEventListener("click", (e) => {
    let codeInput = document.getElementById("acode");
    let passInput = document.getElementById("apass");
    let gencode = generateId();
    let genpass = generatePassword();

    codeInput.value = gencode;
    passInput.value = genpass;
  });

  function generateId(length = 6) {
    const charset = "1234567890";
    let genPass = "";
    for (let i = 0, n = charset.length; i < length; ++i) {
      genPass += charset.charAt(Math.floor(Math.random() * n));
    }
    return genPass;
  }

  function generatePassword(lengths = 8) {
    // Code inspired by a stack overflow post
    const alpha = "abcdefghijklmnopqrstuvwxyz";
    const calpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const num = "1234567890";
    const options = [alpha, alpha, alpha, calpha, calpha, calpha, num, num];
    let pass = "";
    for (let i = 0; i < lengths; i++) {
      opt = Math.floor(Math.random() * options.length);
      choose = Math.floor(Math.random() * options[opt].length);
      pass = pass + options[opt][choose];
      options.splice(opt, 1);
    }
    return pass;
  }
});