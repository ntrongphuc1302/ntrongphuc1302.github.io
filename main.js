// Live clock — header
function updateHeaderClock() {
  const el = document.getElementById("header-clock");
  if (!el) return;
  const now = new Date();
  const hanoi = new Date(now.toLocaleString("en-US", { timeZone: "Asia/Ho_Chi_Minh" }));
  const date = hanoi.toLocaleDateString("en-US", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
  const time = hanoi.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: true,
  });
  el.textContent = date + " " + time + " VN";
}
updateHeaderClock();
setInterval(updateHeaderClock, 1000);

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
