// Keep section navigation and the original discussion tabs usable with a keyboard.
document.querySelectorAll('.tabs').forEach(function (list) {
  const tabs = Array.from(list.querySelectorAll('[role="tab"]'));
  tabs.forEach(function (tab, index) {
    tab.addEventListener('keydown', function (event) {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      tabs[next].click();
      tabs[next].focus();
    });
  });
});
if ('IntersectionObserver' in window) {
  const sections = document.querySelectorAll('main > section[id]');
  const observer = new IntersectionObserver(function (entries) {
    const entry = entries.find(function (item) { return item.isIntersecting; });
    if (!entry) return;
    document.querySelectorAll('nav.toc a').forEach(function (link) {
      const current = link.getAttribute('href') === '#' + entry.target.id;
      link.classList.toggle('is-current', current);
      if (current) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-5% 0px -80% 0px' });
  sections.forEach(function (section) { observer.observe(section); });
}
