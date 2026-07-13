/* Yasto.ma — interactions */
(function () {
  "use strict";

  const WA = "212664140211";
  const WA_URL = "https://wa.me/" + WA;

  /* Mobile nav */
  const toggle = document.querySelector(".menu-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", links.classList.contains("open"));
    });
  }

  /* Accordion */
  document.querySelectorAll(".acc-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const item = btn.closest(".acc-item");
      const open = item.classList.contains("open");
      item.parentElement.querySelectorAll(".acc-item").forEach(function (el) {
        el.classList.remove("open");
        el.querySelector(".acc-btn").setAttribute("aria-expanded", "false");
      });
      if (!open) {
        item.classList.add("open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  /* Counters */
  function animateCounters() {
    document.querySelectorAll("[data-count]").forEach(function (el) {
      const target = parseFloat(el.getAttribute("data-count"));
      const suffix = el.getAttribute("data-suffix") || "";
      const isFloat = String(target).indexOf(".") !== -1;
      const duration = 1600;
      const start = performance.now();

      function tick(now) {
        const p = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - p, 3);
        const val = target * eased;
        el.textContent = (isFloat ? val.toFixed(0) : Math.floor(val).toLocaleString("fr-FR")) + suffix;
        if (p < 1) requestAnimationFrame(tick);
        else el.textContent = (isFloat ? target : target.toLocaleString("fr-FR")) + suffix;
      }
      requestAnimationFrame(tick);
    });
  }

  const counterSection = document.querySelector(".counters");
  if (counterSection && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            animateCounters();
            io.disconnect();
          }
        });
      },
      { threshold: 0.35 }
    );
    io.observe(counterSection);
  } else if (counterSection) {
    animateCounters();
  }

  /* Build WhatsApp message from form */
  function buildMessage(form) {
    const nom = (form.nom && form.nom.value) || "";
    const prenom = (form.prenom && form.prenom.value) || "";
    const indicatif = (form.indicatif && form.indicatif.value) || "+212";
    const telephone = (form.telephone && form.telephone.value) || "";
    const abo = (form.abonnement && form.abonnement.value) || "Non précisé";
    const type = form.getAttribute("data-type") || "test";
    const phone = indicatif + " " + telephone.replace(/\s/g, "");

    if (type === "test") {
      return (
        "Bonjour Yasto.ma 👋%0A" +
        "Je souhaite un *test IPTV Maroc gratuit 24h*.%0A%0A" +
        "*Nom :* " + encodeURIComponent(nom) + "%0A" +
        "*Prénom :* " + encodeURIComponent(prenom) + "%0A" +
        "*Téléphone :* " + encodeURIComponent(phone) + "%0A" +
        "*Abonnement souhaité :* " + encodeURIComponent(abo) + "%0A%0A" +
        "Merci de m'envoyer le lien de test."
      );
    }
    return (
      "Bonjour Yasto.ma 👋%0A" +
      "Je souhaite *acheter un abonnement IPTV Maroc*.%0A%0A" +
      "*Nom :* " + encodeURIComponent(nom) + "%0A" +
      "*Prénom :* " + encodeURIComponent(prenom) + "%0A" +
      "*Téléphone :* " + encodeURIComponent(phone) + "%0A" +
      "*Pack :* " + encodeURIComponent(abo) + "%0A%0A" +
      "Merci de me confirmer l'activation."
    );
  }

  document.querySelectorAll("form[data-whatsapp]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      const msg = buildMessage(form);
      window.open(WA_URL + "?text=" + msg, "_blank", "noopener,noreferrer");
    });
  });

  /* Pack buttons → WhatsApp */
  document.querySelectorAll("[data-pack]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const pack = btn.getAttribute("data-pack");
      const price = btn.getAttribute("data-price") || "";
      const msg =
        "Bonjour Yasto.ma 👋%0A" +
        "Je souhaite commander le pack *" + encodeURIComponent(pack) + "*" +
        (price ? " (" + encodeURIComponent(price) + " DHS)" : "") +
        ".%0A%0AMerci de m'indiquer les modalités d'activation IPTV Maroc.";
      window.open(WA_URL + "?text=" + msg, "_blank", "noopener,noreferrer");
    });
  });

  /* Year */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
