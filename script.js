// =====================================================
// IRCE COACHING — Main JavaScript
// =====================================================

document.addEventListener("DOMContentLoaded", () => {

  // ---------------------------------------------------
  // Mobile menu
  // ---------------------------------------------------

  const menuToggle = document.getElementById("menuToggle");
  const menu = document.querySelector(".menu");

  if (menuToggle && menu) {

    menuToggle.addEventListener("click", () => {
      menu.classList.toggle("mobile-open");
    });

    document.querySelectorAll(".menu a").forEach(link => {
      link.addEventListener("click", () => {
        menu.classList.remove("mobile-open");
      });
    });
  }


  // ---------------------------------------------------
  // Smooth scrolling
  // ---------------------------------------------------

  document.querySelectorAll('a[href^="#"]').forEach(link => {

    link.addEventListener("click", function (event) {

      const targetId = this.getAttribute("href");

      if (!targetId || targetId === "#") {
        return;
      }

      const target = document.querySelector(targetId);

      if (target) {
        event.preventDefault();

        target.scrollIntoView({
          behavior: "smooth",
          block: "start"
        });
      }

    });

  });


  // ---------------------------------------------------
  // Header shadow while scrolling
  // ---------------------------------------------------

  const header = document.querySelector(".header");

  if (header) {

    const updateHeader = () => {

      if (window.scrollY > 20) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }

    };

    window.addEventListener("scroll", updateHeader);

    updateHeader();
  }


  // ---------------------------------------------------
  // Reveal animation
  // ---------------------------------------------------

  const revealElements = document.querySelectorAll(
    ".course-card, .why-card, .exam-item, .contact-card, .about-card"
  );

  if ("IntersectionObserver" in window) {

    const observer = new IntersectionObserver(
      (entries, obs) => {

        entries.forEach(entry => {

          if (entry.isIntersecting) {

            entry.target.classList.add("visible");

            obs.unobserve(entry.target);

          }

        });

      },
      {
        threshold: 0.12
      }
    );

    revealElements.forEach(element => {
      element.classList.add("reveal");
      observer.observe(element);
    });

  } else {

    revealElements.forEach(element => {
      element.classList.add("visible");
    });

  }


  // ---------------------------------------------------
  // Current year
  // ---------------------------------------------------

  const yearElements = document.querySelectorAll("[data-current-year]");

  yearElements.forEach(element => {
    element.textContent = new Date().getFullYear();
  });


  // ---------------------------------------------------
  // Prevent accidental empty links
  // ---------------------------------------------------

  document.querySelectorAll('a[href="#"]').forEach(link => {

    link.addEventListener("click", event => {
      event.preventDefault();
    });

  });

});
