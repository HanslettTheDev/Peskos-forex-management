export function toggleActive(identityClass, cssClassToggle, storageToggleName) {
  let smss = document.querySelector(identityClass + "." + cssClassToggle);
  if (!smss) {
    return
  }
  smss.addEventListener("click", (e) => {
    localStorage.setItem(storageToggleName, e.target.dataset.active);
  });

  const currentActive = localStorage.getItem(storageToggleName);

  if (currentActive) {
    document.querySelectorAll(identityClass).forEach((tab) => {
      if (tab.dataset.active === currentActive) {
        // if (tab.href != window.location.href) {
        //   window.open(tab.href, "_self");
        // }
        tab.classList.add(cssClassToggle);
        localStorage.clear()
        return;
      }
      tab.classList.remove(cssClassToggle);
      localStorage.clear()
    });
  }

  let navTabs = document.querySelectorAll(identityClass);
  navTabs.forEach((tab) => {
    tab.addEventListener("click", toggleTab);
  });

  function toggleTab(e) {
    localStorage.setItem(storageToggleName, e.target.dataset.active);
  }
}


export function paymentsToggleActive() {
    let paymentTabs = document.querySelectorAll(".payments-tab");
    paymentTabs.forEach((tab) => {
        tab.addEventListener("click", e => {
            paymentTabs.forEach((t) => {
                if (t != e.target) {return t.classList.remove("make-active-2")}
            })
            tab.classList.add("make-active-2")
        })
    })
}