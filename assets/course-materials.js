(() => {
  const input = document.getElementById('course-search');
  const cards = [...document.querySelectorAll('[data-study-card]')];
  const topics = [...document.querySelectorAll('[data-study-topic]')];
  if (!input || !cards.length) return;
  document.getElementById('course-filter').hidden = false;
  input.addEventListener('input', () => {
    const query = input.value.trim().toLocaleLowerCase('ko');
    let count = 0;
    cards.forEach(card => {
      card.hidden = !card.textContent.toLocaleLowerCase('ko').includes(query);
      if (!card.hidden) count++;
    });
    topics.forEach(topic => {
      topic.hidden = ![...topic.querySelectorAll('[data-study-card]')].some(card => !card.hidden);
    });
    document.getElementById('course-search-status').textContent = count
      ? `${count}개 학습카드를 표시합니다.`
      : '일치하는 학습카드가 없습니다. 다른 낱말로 찾아보세요.';
  });
})();
