from topic_analyzer import analyze_topics


def compare_trends(today_rows, yesterday_rows=None):

    today = analyze_topics(today_rows)

    if yesterday_rows is None:
        return [
            {
                "topic": topic,
                "today": data["posts"],
                "yesterday": None,
                "change": None,
                "growth": None,
                "status": "비교 데이터 없음"
            }
            for topic, data in today.items()
        ]

    yesterday = analyze_topics(yesterday_rows)

    topics = set(today) | set(yesterday)

    results = []

    for topic in topics:

        current = today.get(topic, {}).get("posts", 0)
        previous = yesterday.get(topic, {}).get("posts", 0)

        change = current - previous

        if previous == 0:
            growth = None
            status = "신규 등장"

        else:
            growth = round(
                (change / previous) * 100, 1
            )

            if current == 0:
                status = "언급 없음"
            elif growth >= 100:
                status = "급상승"
            elif growth > 0:
                status = "상승"
            elif growth < 0:
                status = "하락"
            else:
                status = "유지"

        results.append({
            "topic": topic,
            "today": current,
            "yesterday": previous,
            "change": change,
            "growth": growth,
            "status": status
        })

    return sorted(
        results,
        key=lambda x: (
            x["change"],
            x["today"],
            x["topic"]
        ),
        reverse=True
    )


if __name__ == "__main__":

    from database import load_posts
    from datetime import datetime, timedelta, timezone

    kst = timezone(timedelta(hours=9))

    end = datetime.now(kst).replace(
        hour=11, minute=0,
        second=0, microsecond=0
    )

    if end > datetime.now(kst):
        end -= timedelta(days=1)

    start = end - timedelta(days=1)

    today_rows = [
        row for row in load_posts()
        if start <= datetime.fromisoformat(
            row["created"]
        ) < end
    ]

    # 전일 비교용 가상 데이터
    yesterday_titles = [
        "GTA VI trailer discussion",
        "Valorant tournament",
        "Steam winter sale",
        "Steam winter sale wishlist",
        "League of Legends patch",
        "League of Legends update"
    ]

    yesterday_rows = [
        {
            "title": title,
            "subreddit": "demo",
            "score": 100,
            "comments": 20
        }
        for title in yesterday_titles
    ]

    results = compare_trends(
        today_rows, yesterday_rows
    )

    print("=== GAMING RADAR TREND ANALYSIS ===")
    print("가상 데이터 기반 비교 테스트")
    print(f"금일 게시글: {len(today_rows)}건")
    print(f"전일 게시글: {len(yesterday_rows)}건")
    print()

    for rank, data in enumerate(results, 1):

        growth = data["growth"]

        growth_text = (
            "산정 불가"
            if growth is None
            else f"{growth:+.1f}%"
        )

        print(f"{rank}. {data['topic']}")
        print(f"   전일: {data['yesterday']}건")
        print(f"   금일: {data['today']}건")
        print(f"   증가량: {data['change']:+d}건")
        print(f"   증가율: {growth_text}")
        print(f"   상태: {data['status']}")
        print()
        