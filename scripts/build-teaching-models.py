"""Build the Korean teaching-model comparison from its authored design data."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
models = json.loads((ROOT / 'assets/teaching-model-data.json').read_text(encoding='utf-8'))
assert [m['id'] for m in models] == ['adaptive', 'argument', 'redesign', 'negotiation', 'teach']
e = lambda value: escape(str(value), quote=True)

def flow_text(m):
    return ' → '.join(step['title'] for step in m['flow'])

def default_comparison(m, side):
    pairs = [('시작점',m['start']),('수업 흐름',flow_text(m)),('인공지능 역할',m['ai']),('평가 증거',m['evidence']),('평가 방식',m['evaluation']),('같은 과제에 적용하면',m['commonTask'])]
    rows = ''.join(f'<dt>{e(label)}</dt><dd>{e(value)}</dd>' for label,value in pairs)
    return f'<article class="tm-output" id="compare-{side}-output" data-model="{e(m["id"])}"><h3>{e(m["name"])}</h3><dl>{rows}</dl></article>'

def options(selected):
    return ''.join(f'<option value="{e(m["id"])}"'+(' selected' if m['id']==selected else '')+f'>{e(m["name"])}</option>' for m in models)

def foundation_table(m):
    foundation = m['foundation']
    fields = [('전제와 학습자상', 'premise'), ('학습이 일어나는 기제', 'mechanism'),
              ('사회적 체제와 판단 권한', 'socialSystem'), ('기대하는 직접 효과', 'expectedDirect'),
              ('기대하는 부수적 효과', 'expectedIncidental'), ('지켜야 할 핵심 원리', 'corePrinciples'),
              ('경계 조건과 보완', 'boundaries'), ('최소 적용·검증 계획', 'validationPlan'),
              ('강의 틀과의 연결', 'theoryConnection')]
    rows = []
    for label, key in fields:
        value = foundation[key]
        content = '<ul>' + ''.join(f'<li>{e(item)}</li>' for item in value) + '</ul>' if isinstance(value, list) else e(value)
        rows.append(f'<tr><th scope="row">{e(label)}</th><td>{content}</td></tr>')
    return f'''<details><summary>모형의 전제·원리·성립 조건과 검증 계획</summary><p class="tm-note">{e(foundation['status'])}</p><div class="tm-matrix tm-foundation" role="region" aria-label="{e(m['name'])}의 설계 근거와 적용 조건" tabindex="0"><table><caption>{e(m['name'])} · 수업 흐름이 작동할 조건을 점검하는 설계표</caption><thead><tr><th scope="col">점검할 요소</th><th scope="col">이 모형에서의 설계</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><p class="tm-note">한 번의 수업 전후 기록은 적용 가능성과 변화의 단서를 보여 줍니다. 모형이 변화를 일으켰다는 인과 효과를 입증하려면 비교 조건과 반복 적용을 포함한 별도 연구 설계가 필요합니다.</p></details>'''

cards = ''.join(f'<article class="tm-card" data-model="{e(m["id"])}"><span>0{i+1} · {e(m["unit"])}</span><h3>{e(m["name"])}</h3><p>{e(m["question"])}</p><a href="#{e(m["id"])}">흐름과 평가 펼쳐 보기 →</a></article>' for i,m in enumerate(models))
matrix = ''.join(f'<tr><th scope="row"><a href="#{e(m["id"])}">{e(m["name"])}</a></th><td>{e(m["unit"])}</td><td>{e(flow_text(m))}</td><td>{e(m["evaluation"])}</td></tr>' for m in models)
details = []
for i,m in enumerate(models):
    total = sum(s['minutes'] for s in m['flow'])
    assert total in (40,80,120)
    steps = ''.join(f'<li><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p><small>시간 예시 · {s["minutes"]}분</small></li>' for s in m['flow'])
    criteria = ''.join(f'<li>{e(c)}</li>' for c in m['criteria'])
    details.append(f'''
<article class="tm-model" id="{e(m['id'])}" data-model="{e(m['id'])}">
<header><p class="tm-kicker">0{i+1} · 반복하는 단위: {e(m['unit'])}</p><h2>{e(m['name'])}</h2><p class="tm-lede">{e(m['question'])}</p><p><strong>배울 것:</strong> {e(m['goal'])}</p><p><strong>선택할 때:</strong> {e(m['when'])}</p><p class="tm-note">운영 시간 예시 · {total}분 · 학생의 준비도와 과제 범위에 맞게 조정</p></header>
<ol class="tm-flow" aria-label="{e(m['name'])}의 수업 흐름">{steps}</ol>
<div class="tm-callout"><p><strong>되돌아가는 지점 ↺</strong> {e(m['loop'])}</p><p><strong>다음으로 넘어가는 기준</strong> {e(m['gate'])}</p></div>
<div class="tm-evaluation"><h3>이 모형의 평가 방식</h3><dl><dt>중심 방법</dt><dd>{e(m['evaluation'])}</dd><dt>수집할 증거</dt><dd>{e(m['evidence'])}</dd><dt>판단 기준</dt><dd><ul>{criteria}</ul></dd><dt>개인 확인 문항</dt><dd>{e(m['assessmentPrompt'])}</dd><dt>평가 뒤 지원</dt><dd>{e(m['feedback'])}</dd></dl><p class="tm-note">{e(m['avoid'])}</p></div>
<div class="tm-example"><h3>같은 ‘학교 쉼터’ 과제를 이 모형으로 하면</h3><p>{e(m['commonTask'])}</p></div>
{foundation_table(m)}
<details><summary>몰입·성장과 교사·인공지능의 역할</summary><div class="tm-shared"><article><h3>몰입을 돕는 장치</h3><p>{e(m['immersion'])}</p></article><article><h3>성장에 따른 지원 변화</h3><p>{e(m['growth'])}</p></article><article><h3>교사의 개입</h3><p>{e(m['teacher'])}</p></article><article><h3>인공지능의 협업 역할</h3><p>{e(m['ai'])}</p></article></div><p><strong>준비할 자료:</strong> {e(m['material'])}</p><p><strong>교과에 옮기기:</strong> {e(m['extension'])}</p></details>
<p class="tm-note"><a href="#comparison">다른 모형과 나란히 비교하기 ↑</a></p>
</article>''')

comparison_data = {m['id']:{k:(flow_text(m) if k=='flow' else m[k]) for k in ('name','start','flow','ai','evidence','evaluation','commonTask')} for m in models}
comparison_json = json.dumps(comparison_data, ensure_ascii=False).replace('<','\\u003c')
page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="몰입·성장과 인공지능 협업을 공유하며 수업 흐름과 평가 방법이 다른 다섯 수업모형. 도전 조절, 증거 논증, 실패·재설계, 역할 협상, 가르치며 성장을 비교합니다."><title>다섯 가지 수업모형 비교 · 호모 루덴스</title><link rel="stylesheet" href="./assets/lab.css"><link rel="stylesheet" href="./assets/teaching-models.css"><style>.tm-foundation table{{min-width:0;width:100%}}.tm-foundation th:first-child{{width:27%;min-width:0}}.tm-foundation td{{min-width:0;overflow-wrap:anywhere}}</style></head>
<body><a class="skip-link" href="#main">본문으로 건너뛰기</a><div class="shell"><header class="masthead"><a class="brand" href="./index.html"><span class="brand-mark" aria-hidden="true">✦</span>호모 루덴스</a><nav class="site-nav" aria-label="주 메뉴"><a href="./index.html">홈</a><a href="./teaching-foundations.html">수업모형 기초</a><a href="./g-flipped-learning.html">G-Flipped Learning</a><a href="./science-g-flipped.html">과학 수업 적용</a><a href="./teaching-models.html" aria-current="page">모형 비교</a><a href="./course-materials.html">수업 자료실</a><a href="./korean-study.html">한국어 공부방</a></nav></header>
<main id="main"><header class="tm-hero"><p class="tm-kicker">수업모형 설계실 · 비교 설계안 0.3</p><h1>배움의 원칙은 함께,<br>수업의 구조는 다르게.</h1><p class="tm-lede">몰입·성장과 인공지능 협업을 공통으로 두고,<br><strong>배움을 일으키는 활동과 평가 방식을 다섯 가지로 설계합니다.</strong></p><p>도전, 주장, 시제품, 협상안, 설명. 수업에서 무엇을 반복하고 어떤 증거로 배움을 확인할지에 따라 시작점·활동 순서·교사의 개입·다음 단계로 가는 조건이 달라집니다.</p><nav class="tm-nav" aria-label="수업모형 바로가기"><a href="#overview">다섯 구조 한눈에</a><a href="#comparison">두 모형 나란히 비교</a><a href="#adaptive">모형별 흐름과 평가</a><a href="#choose">수업모형 선택하기</a></nav><p class="tm-note">2026년 11월 24일 · 함께 개발하는 설계 초안입니다. 아래 이름은 비교를 위한 가칭이며, 효과가 검증된 새로운 이론이나 공인된 모형을 뜻하지 않습니다.</p></header>

<section class="tm-section" aria-labelledby="foundation-entry"><p class="tm-kicker">기초에서 설계로</p><h2 id="foundation-entry">수업모형의 조건을 알고, 설계안을 비교하기</h2><p>수업모형은 학습이 일어나는 원리와 구조를 설명하고, 수업 디자인은 이를 학생·교과·시간·환경에 맞게 구체화합니다. 각 설계안 아래에는 전제, 핵심 원리, 역할, 기대 효과와 검증 계획을 함께 적었습니다.</p><div class="tm-footer"><a href="./teaching-foundations.html">수업모형·수업 디자인의 기초 →</a><a href="./course-materials.html">앞부분 강의와 교육자료 전체 보기 →</a></div><p class="tm-note">이 페이지의 다섯 모형은 강의의 분석틀을 적용한 자체 설계 가설이며, 효과가 검증된 모형으로 제시하지 않습니다.</p></section>

<section class="tm-callout" id="game-quest-connection"><h2>이 다섯 구조를 게임 속 학습 미션으로 연결합니다</h2><p><a href="./g-flipped-learning.html">G-Flipped Learning</a>은 사전 게임학습의 진단 자료를 바탕으로 파티·개인 미션·팀 미션을 설계하는 중심 모형입니다. 아래 다섯 구조는 연습, 근거 검토, 실험 개선, 협상, 설명 등 서로 다른 퀘스트를 설계하는 데 사용할 수 있습니다.</p><p><a href="./science-g-flipped.html">기존 과학 수업 사례에 적용하기 →</a></p></section><section class="tm-section" id="shared"><p class="tm-kicker">모든 모형에 남길 공통 원칙</p><h2>선택할 수 있는 도전, 성장에 맞는 지원, 사람의 판단</h2><div class="tm-shared"><article><h3>몰입</h3><p>의미 있는 목표, 학생의 선택, 즉시 쓸 수 있는 피드백, 해 볼 만한 도전을 마련합니다. 활동 자체의 흥미와 학생이 느끼는 어려움을 함께 살핍니다.</p></article><article><h3>성장</h3><p>처음의 생각·수행과 도움에 대한 반응을 보고 지원을 조절합니다. 익숙해지면 도움을 줄이고 조건을 바꿔 스스로 할 수 있는지 확인합니다.</p></article><article><h3>인공지능 협업</h3><p>힌트 제공자·반론자·설계 검토자·관점 제안자·배우는 역할 중 필요한 역할을 줍니다. 학생은 근거를 확인하고 교사와 함께 결정합니다.</p></article><article><h3>배움의 증거</h3><p>공동 결과물과 개인의 배움을 구분합니다. 몰입 경험도 성취와 따로 확인하며, 기초 지식과 독립 수행을 각 모형에 맞는 방식으로 평가합니다.</p></article></div><div class="tm-callout"><strong>공통 원칙은 지키되, 한 가지 순서를 강제하지 않습니다.</strong><p>앞서 만든 여섯 단계는 <a href="./co-learning-model.html#cycle">통합 탐구형의 흐름 예시</a>로 남깁니다. 아래 모형은 반복 단위와 다음 단계로 넘어가는 조건부터 다르게 설계했습니다.</p></div></section>

<section class="tm-section" id="overview"><p class="tm-kicker">수업의 중심 활동을 고르기</p><h2>무엇을 반복하며 배우는가?</h2><div class="tm-cards">{cards}</div><div class="tm-matrix" role="region" aria-label="모형별 수업 흐름과 평가 비교표" tabindex="0"><table><caption>좁은 화면에서는 표를 가로로 밀어 볼 수 있습니다. 아래 두 모형 비교는 세로로도 읽을 수 있습니다.</caption><thead><tr><th scope="col">모형</th><th scope="col">반복하는 활동</th><th scope="col">수업 흐름</th><th scope="col">중심 평가 방식</th></tr></thead><tbody>{matrix}</tbody></table></div></section>

<section class="tm-section" id="comparison"><p class="tm-kicker">같은 소재로 구조의 차이 확인하기</p><h2>두 모형을 나란히 비교하기</h2><p>비교 과제는 모두 <strong>‘학교 쉼터 개선하기’</strong>입니다. 소재를 고정하고 학생이 할 사고와 평가를 바꾸어 봅니다. 모형마다 초점이 되는 학습목표도 달라지므로, 이 비교는 어느 모형의 효과가 더 큰지를 입증하는 실험은 아닙니다.</p><div class="tm-selectors" id="model-selectors" hidden><div><label for="compare-left">왼쪽에서 볼 모형</label><select id="compare-left">{options('adaptive')}</select></div><div><label for="compare-right">오른쪽에서 볼 모형</label><select id="compare-right">{options('argument')}</select></div><p id="compare-status" role="status">도전 조절형과 증거 논증형을 비교합니다.</p></div><noscript><p class="tm-note">현재 도전 조절형과 증거 논증형의 기본 비교를 표시합니다. 자바스크립트를 사용하면 다른 조합을 선택할 수 있습니다. 다섯 모형의 전체 설명은 아래에 있습니다.</p></noscript><div class="tm-compare">{default_comparison(models[0],'left')}{default_comparison(models[1],'right')}</div></section>

<section class="tm-section" id="model-details"><p class="tm-kicker">실제로 운영할 때의 차이</p><h2>흐름·되돌아갈 지점·평가 뒤의 지원까지</h2><p>단계마다 배정한 시간은 운영 예시입니다. 학생의 준비도와 과제 범위를 보고 차시를 나누거나 조정합니다. 모형의 핵심은 시간표보다 반복하는 활동과 판단 기준에 있습니다.</p></section>
{''.join(details)}

<section class="tm-section" id="choose"><p class="tm-kicker">교사가 결정하는 수업 디자인</p><h2>도구보다 먼저, 학생에게 필요한 배움 고르기</h2><div class="tm-chooser"><ol><li><strong>핵심 개념과 절차를 각자 익혀야 한다면</strong> → 도전 조절형. 지원 반응과 독립 수행을 중심으로 봅니다.</li><li><strong>주장을 검토하고 근거로 판단해야 한다면</strong> → 증거 논증형. 출처·추론·반론 대응을 중심으로 봅니다.</li><li><strong>실제 결과를 보고 원리와 방법을 고쳐야 한다면</strong> → 실패·재설계형. 원인 가설과 수정 전후의 증거를 봅니다.</li><li><strong>다른 사람의 필요를 반영해 공동 결정해야 한다면</strong> → 역할 협상형. 관점 이해·절충·결정 책임을 봅니다.</li><li><strong>설명과 오류 진단으로 이해를 깊게 해야 한다면</strong> → 가르치며 성장형. 진단 질문·예와 반례·개인 전이를 봅니다.</li></ol></div><div class="tm-example"><h3>모형을 결합할 때도 평가 목적은 분명하게</h3><p>예를 들어 쉼터 배치를 <strong>실패·재설계형</strong>으로 시험한 뒤, 실제 채택할 안은 <strong>역할 협상형</strong>으로 정할 수 있습니다. 앞에서는 시험과 수정의 타당성을, 뒤에서는 서로 다른 필요를 반영한 결정 근거를 평가합니다. 활동을 늘리기보다 각 단계에서 배울 것과 확인할 증거를 정합니다.</p></div><p>증강현실·스마트 안경은 관찰이나 시험을 돕는 지원 환경으로 선택합니다. 역할 카드·실물·종이로도 핵심 사고를 수행할 수 있게 합니다. 현장·실시간 원격·시간 선택 참여는 <a href="./co-learning-model.html#participation-design">같은 목표와 평가 증거에 이르는 경로</a>로 설계합니다.</p><p class="tm-note">인공지능을 사용할 수 없을 때는 교사가 확인한 힌트·반론·오개념 카드나 동료 역할로 같은 흐름을 운영할 수 있습니다. 인공지능이 실제로 연결된 프로그램은 아니며, 이 페이지의 선택 기능은 작성된 모형을 비교해 보여 줍니다.</p></section>

<section class="tm-section" id="assessment-design"><p class="tm-kicker">평가도 수업모형에 맞춰 설계</p><h2>공통으로 확인할 배움과, 모형마다 다른 증거</h2><p>모든 모형에서 교과 개념 이해와 개인의 독립 수행을 확인합니다. 그 위에 도전 조절형은 <strong>지원에 대한 반응</strong>, 논증형은 <strong>근거와 추론</strong>, 재설계형은 <strong>시험과 개선</strong>, 협상형은 <strong>관점과 절충</strong>, 가르치며 성장형은 <strong>오류 진단과 설명</strong>을 봅니다. 한 가지 채점표를 그대로 복사하지 않습니다.</p><div class="tm-shared"><article><h3>수업 전</h3><p>학습목표, 학생이 직접 수행할 사고, 평가 기준을 공유합니다. 학생의 첫 생각이나 수행으로 출발점을 확인합니다.</p></article><article><h3>수업 중</h3><p>모형의 핵심 장면에서 필요한 증거만 모읍니다. 교사는 그 증거를 다음 질문·지원·역할·과제 조정에 사용합니다.</p></article><article><h3>수업 뒤</h3><p>개인의 새 설명·문제·오류 진단·관점 전환 과제로 배움을 확인합니다. 모둠의 좋은 결과를 모든 학생의 성취로 대신하지 않습니다.</p></article></div><p class="tm-note">학교의 실제 성적 반영은 교과 목표와 평가 계획에 맞춰 정합니다. 이 페이지는 새 평가 도구의 타당도나 모형의 효과가 확인된 결과가 아니라, 함께 시험하고 고칠 설계 초안입니다.</p></section>

<section class="tm-section" id="connections"><p class="tm-kicker">예전 작업에서 이어 온 원리</p><h2>하나의 연구 방향, 여러 수업 구조</h2><p>몰입·역동적 평가의 지원 조절은 도전 조절형에, 공동주체성의 응답 검증은 논증형에, 이야기섬의 관점 교환과 공동 판단은 협상형에, 부기 페르소나의 배우는 인물은 가르치며 성장형에 연결했습니다. 실패·재설계형은 현실에서 직접 만들고 검증하려는 구상을 구체화했습니다.</p><p>이 연결은 기존 작업을 새 설계에 어떻게 활용했는지 설명하는 것입니다. 각 모형의 효과는 목표·학생·조건을 정한 수업 적용에서 따로 살펴야 합니다.</p><div class="tm-footer"><a href="./co-learning-model.html#lineage">찾아 연결한 이전 작업 →</a><a href="./co-learning-model.html#sources">한국어 근거 자료 →</a><a href="./lesson-designs.html">이전에 만든 교과 적용 사례 →</a><a href="./co-learning-model.html#record">내 수업 설계 기록하기 →</a></div></section>
</main><footer class="site-footer"><p>호모 루덴스 · 재미있고 즐겁게 가르치고 배우는 교사를 위하여</p><p>수업모형 비교 설계안 0.3 · 2026년 11월 24일</p></footer></div><script type="application/json" id="model-comparison-data">{comparison_json}</script><script src="./assets/teaching-models.js"></script></body></html>
'''
(ROOT / 'teaching-models.html').write_text(page, encoding='utf-8')
print('Built five teaching models, same-task comparison, and distinct assessment designs.')
