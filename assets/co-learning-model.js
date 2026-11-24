(function(){
  'use strict';
  var participation=document.getElementById('participation');
  var medium=document.getElementById('medium');
  var status=document.getElementById('co-save-status');
  var fields=Array.from(document.querySelectorAll('[data-co-record]'));
  var storageKey='homo-ludens.co-learning.v1';
  var labels={question:'함께 탐구할 문제',goal:'학생이 배워야 할 목표',judgment:'사람이 직접 판단하고 결정할 것',evidence:'평가에서 확인할 증거',next:'다음에 함께 수정할 것'};
  var modes={
    onsite:{title:'현장에서 함께 관찰하고 비교하기',label:'현장 참여',action:'학교 쉼터를 직접 관찰하고 불편한 지점과 이용자의 요구를 기록합니다. 모둠별로 두 개선안을 만들고, 관찰 자료를 근거로 선택을 설명합니다.',materials:'교사가 준비한 공통 사진·도면·이용 조건과 현장 관찰 기록을 함께 사용합니다. 현장에 없는 학생에게도 같은 자료를 전달합니다.',evidence:'관찰 근거, 두 안의 비교표, 선택 이유와 수정 기록을 제출합니다. 마지막에는 각자 새 조건을 받았을 때의 판단을 설명합니다.'},
    live:{title:'실시간으로 연결해 같은 문제 해결하기',label:'실시간 원격 참여',action:'현장 동료가 공유하는 사진과 관찰 기록을 보며 확인할 질문을 보냅니다. 원격 학생도 비교 기준과 개선안을 제안하고 모둠의 최종 선택에 참여합니다.',materials:'공통 사진·도면·이용 조건을 미리 제공합니다. 실시간 연결이 끊기면 같은 자료 묶음으로 이어가고, 놓친 의견은 정해진 시간에 보충합니다.',evidence:'현장 참여와 같은 관찰 근거, 두 안의 비교표, 선택 이유와 수정 기록을 제출합니다. 연결 시간이나 발언 횟수 대신 판단의 근거와 개인의 설명을 확인합니다.'},
    flex:{title:'정해진 기간 안에서 질문하고 고쳐 보기',label:'시간 선택 참여',action:'같은 자료 묶음을 읽고 첫 개선안과 질문을 제출합니다. 정해 둔 교환 기한에 동료나 교사의 회신을 확인하고, 그 의견을 반영해 두 안을 비교하고 수정합니다.',materials:'사진·도면·관찰 메모·이용 조건과 활동 안내를 한 묶음으로 제공합니다. 최초 제출, 질문 교환, 회신, 최종 수정의 기한을 함께 안내합니다.',evidence:'동일한 관찰 근거, 비교표, 선택 이유와 수정 기록을 남깁니다. 회신을 어떻게 받아들이거나 거절했는지와 각자의 최종 설명을 함께 확인합니다.'}
  };
  var media={
    glasses:{label:'스마트 안경·증강현실',action:'현장에서는 기기가 지원하는 범위에서 실제 위치에 짧은 관찰 단서나 확인 순서를 겹쳐 봅니다. 원격·시간 선택 참여자는 같은 사진·도면의 주석으로 안내를 받습니다.',limit:'이 페이지는 스마트 안경과 연결되지 않은 설계 예시입니다. 실제 기기의 표시·공유 기능을 먼저 확인하고, 사용할 수 없으면 같은 사진·도면으로 활동을 이어갑니다.'},
    tablet:{label:'태블릿·스마트폰',action:'공통 사진과 도면에 주석을 달아 불편한 지점, 근거, 개선안을 표시합니다. 현장 사진과 원격 의견을 같은 자료에 연결하고 서로의 판단을 검토합니다.',limit:'특정 기기나 프로그램의 사용 숙련도를 학습 성취로 대신 평가하지 않습니다. 화면 접근이 어려우면 같은 내용을 종이로 제공합니다.'},
    paper:{label:'종이·사진 카드',action:'공통 사진 카드와 도면에 관찰 메모와 두 개선안을 표시합니다. 종이 기록을 전달하거나 사진으로 공유해 동료 질문과 수정 의견을 교환합니다.',limit:'디지털 기기가 없어도 같은 학습 목표와 판단 증거를 남길 수 있게 합니다. 자료 전달과 회신 시점은 참여 방식에 맞춰 교사가 정합니다.'}
  };
  function setText(id,text){var element=document.getElementById(id);if(element)element.textContent=text;}
  function selection(){return{participation:participation&&modes[participation.value]?participation.value:'onsite',medium:medium&&media[medium.value]?medium.value:'tablet'};}
  function render(){var choice=selection(),mode=modes[choice.participation],device=media[choice.medium];setText('mode-title',mode.title);setText('mode-action',mode.action);setText('mode-materials',mode.materials);setText('mode-evidence',mode.evidence);setText('medium-action',device.action);setText('medium-limit',device.limit);}
  function say(message){if(status)status.textContent=message;}
  try{
    var raw=localStorage.getItem(storageKey),saved=raw?JSON.parse(raw):{};
    if(!saved||typeof saved!=='object'||Array.isArray(saved))throw new Error('invalid saved record');
    var records=saved.records&&typeof saved.records==='object'&&!Array.isArray(saved.records)?saved.records:{};
    fields.forEach(function(field){var value=records[field.dataset.coRecord];if(typeof value==='string')field.value=value;});
    if(participation&&modes[saved.participation])participation.value=saved.participation;
    if(medium&&media[saved.medium])medium.value=saved.medium;
  }catch(error){say('저장된 기록을 불러오지 못했습니다. 새로 작성한 내용은 파일로 저장할 수 있습니다.');}
  function save(){var data=selection();data.records={};fields.forEach(function(field){data.records[field.dataset.coRecord]=field.value;});try{localStorage.setItem(storageKey,JSON.stringify(data));say('이 브라우저에 저장했습니다.');}catch(error){say('브라우저 저장을 사용할 수 없습니다. 작성한 기록을 파일로 저장해 주세요.');}}
  [participation,medium].forEach(function(element){if(element)element.addEventListener('change',function(){render();save();});});
  fields.forEach(function(field){field.addEventListener('input',save);});
  var reset=document.getElementById('planner-reset');
  if(reset)reset.addEventListener('click',function(){if(participation)participation.value='onsite';if(medium)medium.value='tablet';render();save();say('참여 방식과 도구를 처음 설정으로 돌렸습니다. 작성한 기록은 유지됩니다.');});
  var exportButton=document.getElementById('co-export');
  if(exportButton)exportButton.addEventListener('click',function(){var choice=selection(),lines=['호모 루덴스 · 함께 판단하고 성장하는 수업모형','함께 공부하고 수정하는 설계 기록','','참여 방식: '+modes[choice.participation].label,'도구: '+media[choice.medium].label,'참여 방식 비교 예시의 목표: 관찰 자료로 두 안을 비교해 선택 근거 설명하기',''];fields.forEach(function(field){lines.push(labels[field.dataset.coRecord]||'설계 메모',field.value,'');});var url=URL.createObjectURL(new Blob(['\uFEFF'+lines.join('\r\n')],{type:'text/plain;charset=utf-8'})),anchor=document.createElement('a');anchor.href=url;anchor.download='호모루덴스_함께판단하는_수업설계.txt';document.body.appendChild(anchor);anchor.click();anchor.remove();setTimeout(function(){URL.revokeObjectURL(url);},1000);say('수업 설계 기록 다운로드를 시작했습니다.');});
  render();
})();
