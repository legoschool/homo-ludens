(function(){
  'use strict';
  var solo=document.getElementById('solo-state'),help=document.getElementById('help-state'),feeling=document.getElementById('feeling-state'),barrier=document.getElementById('barrier-state');
  var scenarios={
    observe:{title:'도움에 어떻게 반응하는지 먼저 확인하기',action:'어디서 막혔는지 듣고, 작은 단서를 하나 제시한 뒤 다시 설명하게 합니다.',task:'같은 공원 배치 과제에서 한 칸의 넓이를 표시해 줍니다. 전체 넓이를 세는 방법은 학생이 찾아보게 합니다.',question:'어떤 점에서 막혔고, 어떤 도움을 받으면 시작할 수 있을까?',evidence:'제공한 도움의 종류, 도움 전후 설명, 학생이 선택한 전략을 함께 남깁니다.'},
    rebuild:{title:'작은 성공이 가능한 출발점 다시 찾기',action:'지시문 이해와 선행 개념을 확인하고, 필요한 부분을 함께 해 본 뒤 학생에게 다시 맡깁니다.',task:'공원의 일부를 모눈으로 제시해 넓이를 함께 세어 봅니다. 이어서 옆 구역은 학생이 세고 방법을 설명하게 합니다.',question:'여기까지는 같이 해 보자. 다음 구역은 어떤 방법으로 해 볼래?',evidence:'직접 보여 준 부분과 학생이 스스로 이어 간 부분을 구분하고, 다음에는 같은 도움이 필요한지 확인합니다.'},
    fade:{title:'같은 목표에서 도움을 줄여 다시 해 보기',action:'힌트로 해결한 전략을 학생의 말로 설명하게 한 뒤, 한 단계 적은 도움으로 비슷한 과제를 제시합니다.',task:'모눈이 있는 공원을 해결했다면 일부 모눈을 가린 비슷한 배치로 바꿉니다. 필요하면 학생이 힌트를 다시 요청할 수 있습니다.',question:'방금 도움이 되었던 방법을 네 말로 설명해 줄래? 이번에는 어느 도움 없이 해 볼 수 있을까?',evidence:'줄인 도움의 내용, 독립적으로 한 설명, 힌트 재요청과 수행의 변화를 기록합니다.'},
    extend:{title:'새 조건을 선택해 배움을 넓히기',action:'다른 형태에서도 설명하는지 확인하고, 학생이 다음 조건이나 표현 방식을 고르게 합니다.',task:'넓이는 같지만 모양이 다른 공원 두 개를 만들어 비교합니다. 그림·모형·말 중 설명 방식을 선택하게 합니다.',question:'넓이는 같은데 모양이 다른 공원을 만들 수 있을까? 어떤 방식으로 증명하고 싶니?',evidence:'도움 없는 새 문제의 근거 설명과 적용 전략을 확인합니다. 너무 쉬웠는지, 도전할 만했는지도 묻습니다.'},
    transfer:{title:'비슷한 새 문제에서 독립 수행 확인하기',action:'처음 문제를 푼 경험이 새로운 배치에도 이어지는지 확인한 뒤 다음 도전을 정합니다.',task:'그림의 방향과 배치가 다른 공원을 제시하고, 넓이가 같은지 혼자 판단해 근거를 설명하게 합니다.',question:'배치가 바뀌어도 같은 방법을 쓸 수 있을까? 왜 그렇게 생각하니?',evidence:'처음 문제의 성공과 새 문제의 성공을 나누어 기록하고, 추가 도움의 필요 여부를 확인합니다.'}
  };
  function render(){
    var id=help.value==='stuck'?'rebuild':help.value==='supported'?'fade':help.value==='transfer'?'extend':solo.value==='independent'?'transfer':'observe';
    var result=scenarios[id];
    ['title','action','task','question','evidence'].forEach(function(k){document.getElementById('next-'+k).textContent=result[k];});
    var feelings={unknown:'학생이 느낀 도전과 즐거움을 짧게 묻습니다. 수행 자료만으로 몰입을 판단하지 않습니다.',ready:'더 해 보고 싶은 마음을 존중하며 전략과 도움의 선택권을 줍니다. 몰입 경험과 학습 결과는 따로 확인합니다.',bored:'지루한 이유를 먼저 듣습니다. 내용 이해를 확인한 뒤 새로운 맥락·표현·역할을 제안하고, 단순히 문제 수만 늘리지 않습니다.',overwhelmed:'잠시 쉬거나 도움을 고를 기회를 줍니다. 부담의 원인을 함께 찾고, 수행에 맞는 지원으로 다시 시작합니다.'};
    document.getElementById('feeling-note').textContent=feelings[feeling.value];
    var barriers={none:'',rules:'먼저 규칙과 지시문을 짧게 보여 주고 한 번 시연합니다. 규칙 이해의 어려움을 교과 능력 부족으로 해석하지 않습니다.',device:'먼저 알림을 줄이고 기기 문제를 해결하거나 종이 과제로 전환합니다. 기기 지연을 학습의 어려움으로 해석하지 않습니다.',voice:'먼저 설명·선택 역할을 순환하고 각자 생각할 시간을 줍니다. 모둠의 성공과 개인의 이해를 따로 확인합니다.'};
    var b=document.getElementById('barrier-note');b.textContent=barriers[barrier.value];b.hidden=!b.textContent;
  }
  [solo,help,feeling,barrier].forEach(function(el){el.addEventListener('change',render);});
  document.getElementById('scenario-reset').addEventListener('click',function(){document.getElementById('scenario-form').reset();render();});render();
  var key='homo-ludens.learning-model.v1',fields=Array.from(document.querySelectorAll('[data-record]')),status=document.getElementById('model-save-status');
  try{var saved=JSON.parse(localStorage.getItem(key)||'{}');fields.forEach(function(f){f.value=typeof saved[f.dataset.record]==='string'?saved[f.dataset.record]:'';});}catch(e){status.textContent='저장된 기록을 불러오지 못했습니다. 작성 후 파일로 저장할 수 있습니다.';}
  function save(){var data={};fields.forEach(function(f){data[f.dataset.record]=f.value;});try{localStorage.setItem(key,JSON.stringify(data));status.textContent='이 브라우저에 저장했습니다.';}catch(e){status.textContent='브라우저에 저장하지 못했습니다. 기록을 파일로 저장해 주세요.';}}
  fields.forEach(function(f){f.addEventListener('input',save);});
  document.getElementById('model-export').addEventListener('click',function(){var lines=['호모 루덴스 · 몰입과 성장이 있는 수업모형','첫 설계안 0.1 · 함께 공부하고 수정할 기록',''];fields.forEach(function(f){lines.push(f.parentElement.firstChild.textContent.trim(),f.value,'');});var a=document.createElement('a'),url=URL.createObjectURL(new Blob(['\uFEFF'+lines.join('\r\n')],{type:'text/plain;charset=utf-8'}));a.href=url;a.download='호모루덴스_수업모형_설계기록.txt';document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(url);},1000);status.textContent='설계 기록 다운로드를 시작했습니다.';});
})();
