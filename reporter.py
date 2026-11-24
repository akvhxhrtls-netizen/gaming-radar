def render(start, end, stats, coverage, rows):
    lines=['# Gaming Radar — 검토용 초안', f'조사 기간: {start} ~ {end}', f'확인된 고유 게시글: {stats["observed"]}건 (전체 투고량 아님)', '전일 대비: 미확인', '', '## 서브레딧별 수집 상태']
    lines += [f'- r/{k}: {stats["communities"].get(k,0)}건 / {v}' for k,v in coverage.items()]
    lines += ['', '## 제목 기반 키워드 후보 (중심 주제 검토 전)']
    lines += [f'- {k}: {v}건' for k,v in stats['candidates']]
    lines += ['', '## 원문 검토 목록']
    lines += [f'- r/{r["subreddit"]} | {r["created"]} | 점수 {r["score"]} | 댓글 {r["comments"]} | {r["title"]} | {r["url"]}' for r in rows]
    lines += ['', '## 추가 검토 필요', '중심 주제 분류, 동의어 통합, 찬반 의견, 공식 발표 교차 검증, e스포츠 및 마케팅 인사이트는 아직 자동 구현되지 않았습니다.']
    return '\n'.join(lines)
