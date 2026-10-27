from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'assets/korean-study-data.json').read_text(encoding='utf-8'))
def e(value):
    return escape(str(value), quote=True)
def link(url, label, secondary=False):
    assert url.startswith('https://')
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer"'+(' class="secondary"' if secondary else '')+f'>{e(label)} <span aria-hidden="true">↗</span></a>'

paper_cards = []
for p in data['papers']:
    free = p['access'] == 'free'
    badges = f'<span class="badge">한국어 본문</span><span class="badge{str() if free else " limited"}">{e(p["access_label"])}</span>'
    links = link(p['direct_url'], '한국어 원문 열기') if free else ''
    links += link(p['landing_url'], '논문 정보·원문 경로', bool(free))
    if p.get('publisher_url'):
        links += link(p['publisher_url'], '학회 원문 안내', True)
    questions = ''.join('<li>'+e(q)+'</li>' for q in p['reading_questions'])
    search = p['title']+' '+ ' '.join(p['authors'])+' '+p['summary']+' '+p['research_type']
    paper_cards.append(f'''<article class="paper-card" id="{e(p['id'])}" data-paper-search="{e(search)}" data-access="{e(p['access'])}">
      <div class="paper-meta">{badges}</div><h3>{e(p['title'])}</h3>
      <p class="citation">{e('·'.join(p['authors']))} · {p['year']} · {e(p['journal'])} · {e(p['pages'])}쪽</p>
      <p>{e(p['summary'])}</p>
      <div class="read-guide"><strong>어디부터 읽을까요?</strong><p>{e(p['guide'])}</p></div>
      <details><summary>읽으며 생각할 질문 두 가지</summary><ul>{questions}</ul></details>
      <details><summary>연구 결과를 읽을 때 함께 볼 점</summary><p>{e(p['caution'])}</p></details>
      <div class="paper-links">{links}</div><p class="access-note">{e(p['access_note'])}</p>
    </article>''')

resource_cards = []
for m in data['materials']:
    if m['id'] == 'boardgame-meta-reading':
        continue
    resource_cards.append(f'''<article class="resource-card" id="{e(m['id'])}">
      <div class="paper-meta"><span class="badge">{e(m['type'])}</span><span class="badge">{e(m['length'])}</span></div>
      <h3>{e(m['title'])}</h3><p class="citation">{e(m['provider'])}</p><p>{e(m['description'])}</p>
      <div class="read-guide"><strong>먼저 볼 부분</strong><p>{e(m['read_first'])}</p></div>
      <div class="paper-links">{link(m['url'],m['link_label'])}</div><p class="access-note">{e(m['access'])}</p></article>''')

material_map = {m['id']:m for m in data['materials']}
paper_map = {p['id']:p for p in data['papers']}
extra_papers = {1:['kim-2020','ahn-2020'],2:['yeom-ahn-2021'],3:['han-2025'],4:['jung-lim-2024'],5:['bae-park-2022'],6:['shin-choe-2025']}
answers = [
    '게임 요소를 이름만 쓰기보다 그 요소가 학생에게 시킬 행동을 적어 보세요. 예를 들어 정답 보상에만 점수를 주는 것과, 풀이 이유를 설명해야 다음 단계로 가는 것은 다른 설계입니다.',
    '선택할 여지, 작은 성취를 알 수 있는 피드백, 친구와 함께할 역할을 살펴보세요. 점수를 못 받아도 무엇을 고쳐 다시 해 볼지 알 수 있어야 다음 행동으로 이어집니다.',
    '모둠의 성공과 개인의 이해를 둘 다 확인할 방법이 필요합니다. 역할을 바꾸어 맡게 하고, 모든 학생이 선택 이유를 설명하도록 하는 것은 가능한 방법의 예입니다.',
    '운이나 속도만으로 성공한다면 규칙을 조정할 여지가 있습니다. 문제의 근거를 설명하거나 서로 다른 풀이를 검토하는 행동을 성공 조건과 연결해 보세요.',
    '만든 결과물만 보지 말고 그 안에 담긴 개념을 학생이 설명하게 해 보세요. 정리 시간에 새 문제 하나를 제시하면 게임 상황을 벗어나서도 이해했는지 살필 수 있습니다.',
    '흥미와 이해는 따로 확인합니다. 재미에 대한 질문과 개념 설명 문제를 함께 두고, 연구에서는 대상·기간·비교 조건을 확인하세요. 간단한 수업 관찰만으로 원인과 결과를 단정하지 않습니다.'
]
sessions=[]
for s in data['sessions']:
    links=[]
    for mid in s['materials']:
        target='kwak-heo-2025' if mid=='boardgame-meta-reading' else mid
        links.append(f'<a href="#{target}">{e(material_map[mid]["title"])} ↓</a>')
    for pid in extra_papers[s['number']]:
        p=paper_map[pid]
        links.append(f'<a href="#{pid}">{e("·".join(p["authors"]))} 논문 안내 ↓</a>')
    sessions.append(f'''<details class="study-session"{ ' open' if s['number']==1 else ''}>
      <summary><span class="session-number">{s['number']:02d}단계</span><span class="session-title">{e(s['title'])}</span><span class="session-time">약 {e(s['time'])}</span><span class="session-toggle" aria-hidden="true">＋</span></summary>
      <div class="session-body"><p>{e(s['concept'])}</p><p class="note">읽을 부분: {e(s['reading'])}</p><div class="reading-list">{''.join(links)}</div>
      <div class="session-grid"><div class="session-box"><h3>직접 해 보기</h3><p>{e(s['activity'])}</p></div><div class="session-box"><h3>내가 이해했는지 확인</h3><p>{e(s['self_check'])}</p></div></div>
      <details class="answer"><summary>생각을 돕는 풀이 보기</summary><p>{e(answers[s['number']-1])}</p></details>
      <label class="completion"><input type="checkbox" data-study-done="{s['number']}" data-title="{e(s['title'])}"><span>{e(s['completion'])} — 완료</span></label>
      <p class="note">{e(s['activity_note'])}</p></div></details>''')

glossary=[('게임 기반 학습','게임의 규칙과 선택을 수행하면서 배우는 방식입니다. 보드게임을 하며 약수와 배수를 판단하는 활동이 한 예입니다.'),('게이미피케이션','일반적인 수업에 도전 과제, 선택, 피드백, 성장 기록 같은 게임 요소를 더하는 설계입니다.'),('내재동기','보상을 받기 위해서만이 아니라 활동 자체가 흥미롭고 의미 있어 참여하려는 마음입니다.'),('성찰·디브리핑','활동 뒤 무엇을 했고 왜 그렇게 생각했는지 돌아보고, 교과 개념과 다음 상황으로 연결하는 과정입니다.'),('문헌 고찰','이미 나온 연구를 모아 무엇을 알고 무엇을 아직 모르는지 정리하는 연구입니다.'),('메타분석','여러 연구의 수치 결과를 함께 분석하는 방법입니다. 모은 연구의 대상과 조건이 얼마나 비슷한지도 살펴야 합니다.'),('효과크기','집단 간 차이나 변화가 어느 정도인지 나타내는 수치입니다. 비교 조건을 모르면 숫자만으로 좋고 나쁨을 판단하기 어렵습니다.'),('비교 집단','새 수업을 경험한 학생들과 비교하기 위해 다른 조건에서 공부한 학생들입니다. 시간과 활동 차이도 확인합니다.'),('타당도','검사나 평가 기준이 알아보려는 내용을 적절하게 다루는지를 살피는 것입니다. 전문가 의견과 학생의 학습 효과는 다른 근거입니다.')]
glossary_html=''.join(f'<div class="glossary-item"><strong>{e(k)}</strong><p>{e(v)}</p></div>' for k,v in glossary)

html=f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="한국어 논문 원문과 쉬운 설명, 공개 수업 자료, 여섯 단계 공부 순서를 모은 호모 루덴스 공부방입니다."><title>한국어 논문·공부방 · 호모 루덴스</title><link rel="stylesheet" href="./assets/lab.css"><link rel="stylesheet" href="./assets/korean-study.css"></head>
<body><a class="skip-link" href="#main">본문으로 건너뛰기</a><div class="shell">
<header class="masthead"><a class="brand" href="./index.html"><span class="brand-mark" aria-hidden="true">✦</span>호모 루덴스</a><nav class="site-nav" aria-label="주 메뉴"><a href="./index.html">홈</a><a href="./learning-model.html">수업모형 만들기</a><a href="./game-design.html">우리 게임 설계</a><a href="./korean-study.html" aria-current="page">한국어 공부방</a><a href="./lesson-2026-10-27.html">오늘의 학습</a><a href="./research.html">연구 노트</a><a href="./dashboard.html">학습실</a></nav></header>
<main id="main"><header class="study-hero"><div class="eyebrow">한국어로 읽고 · 내 수업으로 연결하기</div><h1>한국어 논문·공부방</h1><p class="lede">영어를 읽지 않아도 공부를 이어갈 수 있도록,<br>논문과 수업 자료에 쉬운 설명과 읽을 순서를 붙였습니다.</p><p class="note">이곳의 요약·풀이·질문은 모두 한국어입니다. 논문은 한국어 본문을 확인해 골랐습니다. 외부 원문에 영어 초록이나 표가 함께 있는 경우에는 읽을 한국어 부분을 안내합니다.</p><nav class="study-jumps" aria-label="공부방 바로가기"><a href="#plan">순서대로 공부하기</a><a href="#papers">한국어 논문 {len(data['papers'])}편</a><a href="#materials">공개 학습자료 {len(resource_cards)}개</a><a href="#glossary">어려운 말 풀이</a></nav></header>
<div class="start-strip"><div><span>처음에는</span><strong>요약부터 한 문단</strong><p>논문을 처음부터 끝까지 읽기보다, 어떤 질문에 답한 연구인지 먼저 살펴보세요.</p></div><div><span>읽을 때는</span><strong>내 수업 질문 하나</strong><p>무엇을 가르치고, 학생에게 어떤 행동을 시킬지 떠올리며 읽습니다.</p></div><div><span>읽은 뒤에는</span><strong>바꿔 볼 장면 하나</strong><p>완벽한 수업안보다, 다음 수업에서 시도할 작은 변화를 기록합니다.</p></div></div>
<aside class="callout"><strong>함께 읽는 목적은, 우리 수업모형을 만드는 것</strong><p>논문에서 찾은 근거를 몰입과 성장이 있는 수업으로 옮겨 봅니다. 어떤 도전을 주고, 언제 어떻게 돕고, 무엇을 배웠는지 확인할지 설계한 뒤 학생의 변화를 보며 고칩니다.</p><a href="./learning-model.html#studio">읽은 내용을 수업모형 설계로 연결하기 →</a></aside>
<section class="study-section" id="plan"><h2>여섯 단계로 차근차근</h2><p>한 번에 한 단계씩, 편한 속도로 진행하세요. 시간과 실습은 이 공부방의 제안이며 논문에서 효과를 검증한 프로그램은 아닙니다.</p><div class="progress-line"><strong id="progress-label" aria-live="polite">0 / 6단계 완료</strong><progress id="study-progress" value="0" max="6" aria-label="학습 진행률"></progress><span>체크와 메모는 이 브라우저에 저장</span></div>{''.join(sessions)}</section>
<section class="study-section" id="papers"><h2>한국어로 읽는 논문 원문</h2><p>무료로 열린 원문부터 배치했습니다. 나머지는 공식 논문 정보와 원문 이용 경로를 연결했습니다. 읽기 안내의 쪽수는 원문 파일의 페이지 순서입니다.</p><div class="filters"><label>논문 찾기<input id="paper-query" type="search" placeholder="제목·저자·주제 검색" autocomplete="off"></label><label>원문 이용<select id="paper-access"><option value="all">전체 논문</option><option value="free">무료 원문 확인</option><option value="library">기관·원문 경로 확인</option></select></label><span id="paper-count" class="result-count" aria-live="polite">{len(data['papers'])}편</span></div><div class="paper-grid">{''.join(paper_cards)}</div><p id="paper-empty" class="no-results" hidden>검색 결과가 없습니다. 검색어를 줄이거나 원문 이용을 ‘전체 논문’으로 바꿔 보세요.</p></section>
<section class="study-section" id="materials"><h2>논문과 함께 볼 공개 학습자료</h2><p>한국어 강좌와 강의자료, 실제 수업사례를 연결했습니다. 영상은 강좌 안내와 이용 조건을 확인했으며, 전체 영상의 재생을 검증한 것은 아닙니다.</p><div class="resource-grid">{''.join(resource_cards)}</div></section>
<section class="study-section" id="glossary"><h2>어려운 말, 쉬운 한국어로</h2><div class="glossary-grid">{glossary_html}</div></section>
<section class="study-section" id="record"><h2>오늘 남길 공부 기록</h2><p>논문의 문장을 그대로 옮기기보다 내 말로 적어 보세요. 기록은 공개되지 않으며, 사용 중인 브라우저에 저장됩니다.</p><div class="study-record"><label for="study-memo">오늘 이해한 것과 아직 남은 질문</label><textarea id="study-memo" placeholder="예: 모둠으로 앉히는 것과 협력하도록 규칙을 만드는 것은 다르다."></textarea><label for="study-plan">내 수업에 적용할 한 가지</label><textarea id="study-plan" placeholder="예: 정답을 맞힌 친구가 아니라 설명을 아직 하지 않은 친구에게 다음 설명 역할을 맡긴다."></textarea><div class="record-controls"><button type="button" id="export-study">공부 기록을 파일로 저장</button><span id="save-status" role="status">이 브라우저에 자동 저장됩니다.</span></div></div></section>
<p class="study-source-note">자료 확인일: 2026년 10월 27일. 논문 요약은 공개 원문·공식 서지와 보유 원문을 대조해 작성했습니다. 무료 원문 열람과 기관 이용 경로를 구분했으며, 논문 파일을 이 사이트에 재게시하지 않았습니다. 논문 제목 속 영문 표기는 화면에서 한국어로 풀어 적었습니다. 각 카드의 연결에서 원래 서지와 원문을 확인할 수 있습니다.</p></main>
<footer class="site-footer"><p>호모 루덴스 · 재미있고 즐겁게 가르치고 배우는 교사를 위하여</p><a href="./index.html">홈으로 돌아가기 ↑</a></footer></div><script src="./assets/korean-study.js"></script></body></html>'''
(ROOT / 'korean-study.html').write_text(html,encoding='utf-8')
print(f'Built Korean study page: {len(data["papers"])} papers, {len(resource_cards)} learning resources, {len(sessions)} sessions.')
