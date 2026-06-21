// Scroll reveal
const reveals = document.querySelectorAll(".reveal");
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: "0px 0px -30px 0px" }
);
reveals.forEach((el) => revealObserver.observe(el));

// Typed effect — terminal style
const typedEl = document.getElementById("typed-text");
const phrase = "$ hello world";
let i = 0;

function typeChar() {
  if (i <= phrase.length) {
    typedEl.textContent = phrase.substring(0, i);
    i++;
    setTimeout(typeChar, i <= phrase.length ? 90 : 1800);
  } else {
    setTimeout(() => {
      i = 0;
      typeChar();
    }, 4000);
  }
}
typeChar();
