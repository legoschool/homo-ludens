(function(){
  'use strict';
  var select=document.getElementById('lesson-type'),filter=document.getElementById('design-filter'),count=document.getElementById('design-count');
  var lessons=Array.from(document.querySelectorAll('[data-design]'));
  if(!select||!filter||!lessons.length)return;
  var types=lessons.map(function(lesson){return lesson.dataset.design;});
  function show(type){if(type!=='all'&&types.indexOf(type)===-1)type='all';select.value=type;var visible=0;lessons.forEach(function(lesson){lesson.hidden=type!=='all'&&lesson.dataset.design!==type;if(!lesson.hidden)visible++;});if(count)count.textContent=visible+'개 수업을 보고 있습니다.';}
  filter.hidden=false;
  select.addEventListener('change',function(){show(select.value);});
  var all=document.getElementById('show-all');if(all)all.addEventListener('click',function(){show('all');});
  document.querySelectorAll('.design-overview a').forEach(function(link){link.addEventListener('click',function(){var type=link.getAttribute('href').slice(1);show(type);});});
  function matchHash(){var type=location.hash.slice(1);if(types.indexOf(type)!==-1)show(type);}
  window.addEventListener('hashchange',matchHash);matchHash();
})();
