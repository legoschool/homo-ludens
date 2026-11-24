(function(){
  'use strict';
  var dataElement=document.getElementById('model-comparison-data');
  var left=document.getElementById('compare-left');
  var right=document.getElementById('compare-right');
  var status=document.getElementById('compare-status');
  var allowed=['adaptive','argument','redesign','negotiation','teach'];
  var rows=[['start','시작점'],['flow','수업 흐름'],['ai','인공지능 역할'],['evidence','평가 증거'],['evaluation','평가 방식'],['commonTask','같은 과제에 적용하면']];
  if(!dataElement||!left||!right)return;
  var data;
  try{data=JSON.parse(dataElement.textContent);}catch(error){if(status)status.textContent='비교 자료를 불러오지 못했습니다. 아래의 기본 비교와 모형별 설명을 읽어 주세요.';return;}
  function content(value){return Array.isArray(value)?value.join(' → '):(typeof value==='string'?value:'');}
  function valid(key){return allowed.indexOf(key)!==-1&&Object.prototype.hasOwnProperty.call(data,key)&&data[key]&&typeof data[key].name==='string'&&rows.every(function(row){return content(data[key][row[0]]).length>0;});}
  if(!data||typeof data!=='object'||!allowed.every(valid)){if(status)status.textContent='일부 비교 자료가 없어 기본 비교를 표시합니다. 모형별 상세 설명을 확인해 주세요.';return;}
  var selectors=document.getElementById('model-selectors');
  if(selectors)selectors.hidden=false;
  function render(key,id){
    var output=document.getElementById(id);
    if(!output||!valid(key))return;
    var model=data[key],fragment=document.createDocumentFragment(),heading=document.createElement('h3'),list=document.createElement('dl');
    heading.textContent=model.name;
    fragment.appendChild(heading);
    rows.forEach(function(row){var term=document.createElement('dt'),description=document.createElement('dd');term.textContent=row[1];description.textContent=content(model[row[0]]);list.appendChild(term);list.appendChild(description);});
    fragment.appendChild(list);
    output.replaceChildren(fragment);
    output.setAttribute('data-model',key);
  }
  function update(){
    var first=valid(left.value)?left.value:'adaptive',second=valid(right.value)?right.value:'argument';
    left.value=first;right.value=second;
    render(first,'compare-left-output');render(second,'compare-right-output');
    if(status)status.textContent=first===second?'양쪽에 같은 모형을 선택했습니다. 서로 다른 흐름과 평가를 비교하려면 한쪽 모형을 바꿔 주세요.':data[first].name+'과 '+data[second].name+'의 흐름과 평가를 비교하고 있습니다.';
  }
  left.addEventListener('change',update);
  right.addEventListener('change',update);
  update();
})();
