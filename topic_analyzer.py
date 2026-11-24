import re

# 게임명 및 이슈별 유사 표현 사전
TOPIC_ALIASES = {
    "GTA 6": [
        "gta 6", "gta vi", "gta6",
        "grand theft auto 6",
        "grand theft auto vi"
    ],
    "League of Legends": [
        "league of legends", "lol"
    ],
    "Valorant": [
        "valorant"
    ],
    "Counter-Strike 2": [
        "counter-strike 2", "counter strike 2", "cs2"
    ],
    "PUBG": [
        "pubg", "playerunknown's battlegrounds"
    ],
    "Steam Winter Sale": [
        "steam winter sale", "steam winter sales"
    ],
    "Indie Game Marketing": [
        "indie game marketing",
        "indie marketing"
    ],
    "Esports": [
        "esports", "e-sports", "e sports"
    ]
}


def detect_topics(title):
    title = title.lower()
    matched = []

    for topic, aliases in TOPIC_ALIASES.items():
        for alias in aliases:
            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, title):
                matched.append(topic)
                break

    return matched


def analyze_topics(rows):
    results = {}

    for row in rows:
        topics = detect_topics(row["title"])

        for topic in topics:
            if topic not in results:
                results[topic] = {
                    "posts": 0,
                    "score": 0,
                    "comments": 0,
                    "communities": set()
                }

            results[topic]["posts"] += 1
            results[topic]["score"] += row["score"]
            results[topic]["comments"] += row["comments"]
            results[topic]["communities"].add(
                row["subreddit"]
            )

    for topic in results:
        results[topic]["communities"] = sorted(
            results[topic]["communities"]
        )

    return dict(sorted(
        results.items(),
        key=lambda item: (
            item[1]["posts"],
            item[1]["comments"]
        ),
        reverse=True
    ))


if __name__ == "__main__":
    from database import load_posts

    rows = load_posts()
    results = analyze_topics(rows)

    print("=== GAMING RADAR TOPIC ANALYSIS ===")
    print(f"분석 대상 게시글: {len(rows)}건")
    print()

    for rank, (topic, data) in enumerate(
        results.items(), 1
    ):
        print(f"{rank}. {topic}")
        print(f"   게시글 수: {data['posts']}건")
        print(f"   총 점수: {data['score']:,}")
        print(f"   총 댓글 수: {data['comments']:,}")
        print(
            "   관련 커뮤니티: "
            + ", ".join(data["communities"])
        )
        print()
        