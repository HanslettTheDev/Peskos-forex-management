// Active class

document.addEventListener("DOMContentLoaded", () => {

  let smss = document.querySelector(".make-active");
  smss.addEventListener("click", (e) => {
    localStorage.setItem("isActive", e.target.dataset.active);
  });

  const currentActive = localStorage.getItem("isActive");

  if (currentActive) {
    document.querySelectorAll(".nav-tab-items").forEach(tab => {
      if (tab.dataset.active === currentActive) {
        if (tab.href != window.location.href) {
          window.open(tab.href, "_self");
        }
        tab.classList.add("make-active");
        return;
      }
      tab.classList.remove("make-active");
    });

  }

  let navTabs = document.querySelectorAll(".nav-tab-items");
  navTabs.forEach(tab => {
    tab.addEventListener("click", toggleTab)
  });

  function toggleTab(e) {
    localStorage.setItem("isActive", e.target.dataset.active)
  }
})

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

  // check if the email exists already in the database

  const mainForm = document.getElementById("admin-form");
  const errorBox = document.getElementById("error-text");


  mainForm.addEventListener("submit", checkMail);

  async function checkMail(e) {
    await e.preventDefault();
    let mailField = document.getElementById("mail").value;
    await axios.post("/dashboard/admins/check_mail", {
      mail: mailField
    }).then(response => {
      mainForm.submit();
    }).catch((error) => {
      errorBox.classList.add("is-danger")
      errorBox.classList.remove("is-hidden")
      errorBox.textContent = error.response.data
    })
  }



});