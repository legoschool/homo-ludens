(function(){
  'use strict';
  var key='homo-ludens.korean-study.v1';
  var checks=Array.from(document.querySelectorAll('[data-study-done]'));
  var memo=document.getElementById('study-memo'),plan=document.getElementById('study-plan');
  var status=document.getElementById('save-status');
  function progress(){var n=checks.filter(function(c){return c.checked;}).length;document.getElementById('study-progress').value=n;document.getElementById('progress-label').textContent=n+' / '+checks.length+'단계 완료';}
  try{var saved=JSON.parse(localStorage.getItem(key)||'{}');checks.forEach(function(c){c.checked=!!(saved.done&&saved.done[c.dataset.studyDone]);});memo.value=typeof saved.memo==='string'?saved.memo:'';plan.value=typeof saved.plan==='string'?saved.plan:'';}catch(e){status.textContent='브라우저 기록을 불러오지 못했습니다. 작성한 내용은 파일로 저장할 수 있습니다.';}
  progress();
  function save(){var done={};checks.forEach(function(c){done[c.dataset.studyDone]=c.checked;});try{localStorage.setItem(key,JSON.stringify({done:done,memo:memo.value,plan:plan.value}));status.textContent='이 브라우저에 저장했습니다.';}catch(e){status.textContent='브라우저 저장을 사용할 수 없습니다. 기록을 파일로 저장해 주세요.';}progress();}
  checks.forEach(function(c){c.addEventListener('change',save);});memo.addEventListener('input',save);plan.addEventListener('input',save);
  document.getElementById('export-study').addEventListener('click',function(){var lines=['호모 루덴스 · 한국어 논문 공부 기록',''];checks.forEach(function(c){lines.push((c.checked?'[완료] ':'[  ] ')+c.dataset.title);});lines.push('','오늘 이해한 것과 남은 질문',memo.value,'','내 수업에 적용할 한 가지',plan.value);var a=document.createElement('a'),u=URL.createObjectURL(new Blob(['\uFEFF'+lines.join('\r\n')],{type:'text/plain;charset=utf-8'}));a.href=u;a.download='호모루덴스_한국어_공부기록.txt';document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u);},1000);status.textContent='공부 기록 다운로드를 시작했습니다.';});
  var query=document.getElementById('paper-query'),access=document.getElementById('paper-access');
  var papers=Array.from(document.querySelectorAll('[data-paper-search]'));
  function filter(){var q=query.value.trim().toLocaleLowerCase('ko'),n=0;papers.forEach(function(p){var show=(!q||p.dataset.paperSearch.toLocaleLowerCase('ko').includes(q))&&(access.value==='all'||p.dataset.access===access.value);p.hidden=!show;if(show)n++;});document.getElementById('paper-count').textContent=n+'편';document.getElementById('paper-empty').hidden=n!==0;}
  query.addEventListener('input',filter);access.addEventListener('change',filter);filter();
})();
