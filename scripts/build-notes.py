"""Create the standalone research note from the original public artifact snapshot."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'sources/claude-frame.html').read_text(encoding='utf-8')
# The frame wrapper belongs to Claude's hosting environment, not the user's document.
source = source[source.index('<title>'):]
head, body = source.split('<div class="wrap">', 1)
head = head.replace('<title>AI 보드게임 연구 노트</title>', '<title>AI 보드게임 연구 노트 · 호모 루덴스</title>')
head += '''
<meta name="description" content="AI 보드게임 연구 노트와 게이미피케이션 선행연구 대시보드. 논문, 번역, PSMA 수업모형, 학습 퀘스트와 연구 도구를 함께 봅니다.">
<link rel="stylesheet" href="./assets/notes-integration.css">
'''
body = '<div class="wrap">' + body
body = body.replace('<main>', '<main id="main-content">', 1)
body = body.replace('<main id="main-content">', '<main id="main-content">\n<aside class="callout"><strong>한국어로 차근차근 공부하기</strong><p>쉬운 설명과 한국어 논문 원문, 읽을 순서를 모았습니다. <a href="./korean-study.html">한국어 논문·공부방으로 이동 →</a></p></aside>', 1)
body = body.replace('https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js', './assets/marked-4.3.0.min.js')
masthead = '''
<a class="skip-link" href="#main-content">본문으로 건너뛰기</a>
<header class="lab-masthead">
  <a class="lab-title" href="./index.html"><span aria-hidden="true">✦</span> 호모 루덴스</a>
  <nav aria-label="연구실 메뉴">
    <a href="./index.html">홈</a>
    <a href="./korean-study.html">한국어 공부방</a>
    <a href="./lesson-2026-10-27.html">오늘의 학습</a>
    <a href="./research.html" aria-current="page">연구 노트</a>
    <a href="./dashboard.html">학습실</a>
  </nav>
</header>
'''
bridge = '''
<aside class="study-bridge" aria-labelledby="study-bridge-title">
  <div class="study-bridge-kicker">연구와 수업 실천</div>
  <h2 id="study-bridge-title">연구의 맥락에서, 근거를 읽고 설계하는 단계로.</h2>
  <p>이 노트에서 AI 보드게임 연구의 방향을 잡고, 통합한 학습실에서 선행연구를 탐색하고 학습 기록과 설계 초안을 이어 가세요.</p>
  <div class="study-shortcuts">
    <a href="./dashboard.html#library"><span>01 · 논문 읽기</span><strong>선행연구 서재</strong><small>핵심 근거와 논문 탐색 →</small></a>
    <a href="./dashboard.html#quests"><span>02 · 학습 이어가기</span><strong>학습 퀘스트</strong><small>체크리스트와 학습 메모 →</small></a>
    <a href="./dashboard.html#drafts"><span>03 · 연구 구체화</span><strong>수업 설계 초안</strong><small>여덟 가지 설계안 비교 →</small></a>
  </div>
  <a class="study-all" href="./dashboard.html#guide">학습실 이용 가이드와 전체 도구 보기 <span aria-hidden="true">↗</span></a>
</aside>
'''
body = body.replace('</header>', '</header>\n' + bridge, 1)
related = {
    'core': ('핵심 개념을 더 익히려면', 'concept', '개념 비교·분류 학습'),
    'glossary': ('용어를 학습으로 이어가려면', 'dict', '게이미피케이션 용어·개념 사전'),
    'course': ('수업 설계의 근거를 정리하려면', 'methods', '연구 방법 교실'),
    'model': ('설계 초안을 비교하려면', 'drafts', '연구·수업 설계 초안'),
    'roadmap': ('읽기 순서를 학습 기록으로 남기려면', 'quests', '학습 퀘스트'),
    'domestic': ('국내 선행연구를 더 찾아보려면', 'korea', '국내 논문 탐색'),
    'papers': ('핵심 논문과 효과크기를 비교하려면', 'effects', '효과크기 분석'),
    'check': ('남은 확인 과제를 정리하려면', 'todo', '다음 연구 과제'),
}
for section_id, (intro, route, label) in related.items():
    pattern = rf'(<section id="{section_id}"[^>]*>.*?</h2>)'
    callout = f'<p class="related-tool">{intro} <a href="./dashboard.html#{route}">{label} →</a></p>'
    body, count = re.subn(pattern, lambda m: m.group(1) + callout, body, count=1, flags=re.S)
    assert count == 1, section_id
body = body.replace('</body></html>', '<script src="./assets/notes-integration.js"></script>\n</body></html>')
result = '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n' + head + '\n</head>\n<body>\n' + masthead + body
assert '__FRAME_PREAMBLE' not in result
assert result.count('<body>') == 1
assert result.count('</head>') == 1
assert result.count('<section id=') == 12
(ROOT / 'research.html').write_text(result, encoding='utf-8')
print('Built research.html with 12 research sections and 8 links to dashboard tools.')
