
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import Counter

from database import load_posts
from analyzer import summarize
from topic_analyzer import analyze_topics
from trend_analyzer import compare_trends
from discovery import discover_topics
from topic_merger import merge_topics
from issue_classifier import classify_posts
from issue_classifier import summarize_categories


def main():

    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst)

    all_rows = load_posts()

    # 가상 데이터 전용 실행
    if not all_rows:
        print("저장된 테스트 데이터가 없습니다.")
        return

    if any(
        not row["url"].startswith("https://example.com/")
        for row in all_rows
    ):
        raise ValueError("가상 데이터만 사용할 수 있습니다.")

    # 마지막 테스트 데이터 기준으로 분석 기간 설정
    latest = max(
        datetime.fromisoformat(row["created"])
        for row in all_rows
    ).astimezone(kst)

    end = latest.replace(
        hour=11, minute=0, second=0, microsecond=0
    )

    if latest >= end:
        end += timedelta(days=1)

    start = end - timedelta(days=1)
    previous_start = start - timedelta(days=1)

    rows = [
        row for row in all_rows
        if start <= datetime.fromisoformat(
            row["created"]
        ) < end
    ]

    previous_rows = [
        row for row in all_rows
        if previous_start <= datetime.fromisoformat(
            row["created"]
        ) < start
    ]

    # 분석 모듈 통합
    stats = summarize(rows)
    topics = analyze_topics(rows)

    trends = compare_trends(
        rows,
        previous_rows if previous_rows else None
    )

    discovered = discover_topics(rows)
    emerging = merge_topics(discovered)

    classified = classify_posts(rows)
    categories = summarize_categories(classified)

    communities = Counter(
        row["subreddit"] for row in rows
    )

    lines = [
        "# GAMING RADAR",
        "## DAILY GAMING INTELLIGENCE REPORT",
        "",
        "**가상 데이터 기반 테스트 보고서**",
        "",
        f"생성 일시: {now:%Y-%m-%d %H:%M} KST",
        f"조사 기간: {start:%Y-%m-%d %H:%M}"
        f" ~ {end:%Y-%m-%d %H:%M} KST",
        "",
        "---",
        "",
        "## 1. Executive Summary",
        "",
        f"- 분석 게시글: {len(rows)}건",
        f"- 관측 커뮤니티: {len(communities)}개",
        f"- 등록 주제: {len(topics)}개",
        f"- 신규 주제 후보: {len(emerging)}개",
        "- 심층 이슈 요약: AI 분석 대기",
        "",
        "## 2. Data Overview",
        "",
        "| 커뮤니티 | 게시글 수 |",
        "|---|---:|"
    ]

    for name, count in communities.most_common():
        lines.append(f"| r/{name} | {count} |")

    lines.extend([
        "",
        "## 3. Trending Topics",
        "",
        "| 순위 | 주제 | 게시글 | 점수 | 댓글 |",
        "|---:|---|---:|---:|---:|"
    ])

    for rank, (topic, data) in enumerate(
        topics.items(), 1
    ):
        lines.append(
            f"| {rank} | {topic} | "
            f"{data['posts']} | "
            f"{data['score']:,} | "
            f"{data['comments']:,} |"
        )

    lines.extend([
        "",
        "## 4. Daily Growth",
        "",
        "| 주제 | 전일 | 금일 | 증가율 | 상태 |",
        "|---|---:|---:|---:|---|"
    ])

    for item in trends:

        growth = (
            "산정 불가"
            if item["growth"] is None
            else f"{item['growth']:+.1f}%"
        )

        previous = (
            "미확인"
            if item["yesterday"] is None
            else item["yesterday"]
        )

        lines.append(
            f"| {item['topic']} | "
            f"{previous} | "
            f"{item['today']} | "
            f"{growth} | "
            f"{item['status']} |"
        )

    lines.extend([
        "",
        "※ 비교 수치는 저장된 가상 표본 기준입니다.",
        "",
        "## 5. Emerging Topics",
        ""
    ])

    if not emerging:
        lines.append("신규 주제 후보 없음")

    for item in emerging:

        lines.extend([
            f"### {item['topic']}",
            f"- 게시글: {item['posts']}건",
            f"- 점수: {item['score']:,}",
            f"- 댓글: {item['comments']:,}",
            "- 커뮤니티: "
            + ", ".join(item["communities"]),
            "- 통합 표현: "
            + (", ".join(item["aliases"]) or "없음"),
            "- 관련 링크:"
        ])

        for link in item["links"]:
            lines.append(f"  - {link}")

        lines.append("")

    lines.extend([
        "",
        "## 6. Issue Classification",
        "",
        "| 이슈 유형 | 게시글 수 |",
        "|---|---:|"
    ])

    for category, count in categories:
        lines.append(f"| {category} | {count} |")

    lines.extend([
        "",
        "※ 복수 분류 허용",
        "",
        "## 7. Consumer Sentiment",
        "",
        "AI 분석 대기",
        "",
        "## 8. Marketing Insights",
        "",
        "AI 분석 대기",
        "",
        "## 9. eSports Insights",
        "",
        "AI 심층 분석 대기",
        "",
        "### e스포츠 관련 게시글 후보",
        ""
    ])

    for row in classified:

        labels = [
            item["category"]
            for item in row["categories"]
        ]

        if "e스포츠" in labels:
            lines.append(
                f"- [{row['title']}]({row['url']})"
            )

    lines.extend([
        "",
        "## 10. Sources",
        ""
    ])

    for row in rows:

        lines.extend([
            f"### {row['title']}",
            f"- 커뮤니티: r/{row['subreddit']}",
            f"- 작성 일시: {row['created']}",
            f"- 점수: {row['score']}",
            f"- 댓글: {row['comments']}",
            f"- 링크: {row['url']}",
            ""
        ])

    lines.extend([
        "## 11. Limitations",
        "",
        "- 현재 데이터는 가상 데이터입니다.",
        "- 실제 Reddit API는 연결되지 않았습니다.",
        "- 전체 Reddit 게시량을 의미하지 않습니다.",
        "- 주제 및 이슈 분류는 제목 기반입니다.",
        "- 신규 주제 후보는 추가 검토가 필요합니다.",
        "- 동일 게시글은 여러 주제에 포함될 수 있습니다.",
        "- 실제 AI 분석은 수행되지 않았습니다.",
        "- 댓글 수는 긍정 또는 부정 여론을 의미하지 않습니다."
    ])

    folder = Path(__file__).parent / "reports"
    folder.mkdir(exist_ok=True)

    filename = folder / (
        f"Gaming_Radar_DEMO_{end:%Y-%m-%d}.md"
    )

    filename.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    print("=== GAMING RADAR INTEGRATED REPORT ===")
    print("가상 데이터 기반 통합 보고서")
    print()
    print(f"분석 게시글: {len(rows)}건")
    print(f"관측 커뮤니티: {len(communities)}개")
    print(f"등록 주제: {len(topics)}개")
    print(f"신규 주제 후보: {len(emerging)}개")
    print(f"이슈 유형: {len(categories)}개")
    print(f"전일 비교 데이터: {len(previous_rows)}건")
    print()
    print("통합 보고서 생성 완료")
    print(f"저장 위치: {filename}")
    print()
    print("※ 실제 Reddit 및 AI API 호출 없음")


if __name__ == "__main__":
    main()
