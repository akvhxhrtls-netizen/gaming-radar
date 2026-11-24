import re
from collections import defaultdict
from analyzer import STOP
from topic_analyzer import TOPIC_ALIASES

STOP_WORDS = STOP | set(
    "about after before will would should could "
    "your our their more most some any all "
    "really very much many there here been "
    "than then when where which who into "
    "out up down not but also".split()
)

KNOWN_ALIASES = {
    alias.lower()
    for aliases in TOPIC_ALIASES.values()
    for alias in aliases
}


def extract_phrases(title):

    words = re.findall(
        r"[a-z0-9]+(?:[-'][a-z0-9]+)*",
        title.lower()
    )

    phrases = set()

    for size in range(2, 5):

        for i in range(len(words) - size + 1):

            group = words[i:i + size]

            if group[0] in STOP_WORDS:
                continue

            if group[-1] in STOP_WORDS:
                continue

            phrase = " ".join(group)

            if any(
                re.search(
                    r"\b" + re.escape(alias) + r"\b",
                    phrase
                )
                for alias in KNOWN_ALIASES
            ):
                continue

            phrases.add(phrase)

    return phrases


def discover_topics(rows, min_posts=2):

    results = defaultdict(lambda: {
        "posts": 0,
        "score": 0,
        "comments": 0,
        "communities": set(),
        "links": []
    })

    seen_urls = set()

    for row in rows:

        if row["url"] in seen_urls:
            continue

        seen_urls.add(row["url"])

        phrases = extract_phrases(row["title"])

        for phrase in phrases:

            data = results[phrase]

            data["posts"] += 1
            data["score"] += row["score"]
            data["comments"] += row["comments"]

            data["communities"].add(
                row["subreddit"]
            )

            data["links"].append(row["url"])

    candidates = []

    for phrase, data in results.items():

        if data["posts"] < min_posts:
            continue

        data["communities"] = sorted(
            data["communities"]
        )

        candidates.append({
            "topic": phrase,
            **data
        })

    candidates.sort(
        key=lambda x: (
            x["posts"],
            len(x["communities"]),
            x["comments"],
            len(x["topic"])
        ),
        reverse=True
    )

    return candidates


if __name__ == "__main__":

    # 실제 Reddit 데이터가 아닌 가상 테스트 데이터

    titles = [
        ("gaming", "Project Orion gameplay reveal"),
        ("Games", "Project Orion release date"),
        ("pcgaming", "Project Orion system requirements"),
        ("gaming", "AI voice acting controversy"),
        ("gamedev", "AI voice acting debate"),
        ("Games", "GTA 6 trailer discussion"),
        ("pcgaming", "GTA 6 performance concerns")
    ]

    rows = []

    for i, (subreddit, title) in enumerate(titles):

        rows.append({
            "subreddit": subreddit,
            "title": title,
            "score": 100 * (i + 1),
            "comments": 20 * (i + 1),
            "url": f"https://example.com/discovery/{i+1}"
        })

    results = discover_topics(rows)

    print("=== GAMING RADAR DISCOVERY ===")
    print("가상 데이터 기반 신규 주제 탐색")
    print(f"분석 게시글: {len(rows)}건")
    print(f"발견된 후보: {len(results)}개")
    print()

    for rank, data in enumerate(results, 1):

        print(f"{rank}. {data['topic']}")
        print(f"   게시글: {data['posts']}건")
        print(f"   총 점수: {data['score']:,}")
        print(f"   댓글 수: {data['comments']:,}")

        print(
            "   커뮤니티: "
            + ", ".join(data["communities"])
        )

        print("   관련 링크:")

        for link in data["links"]:
            print(f"   - {link}")

        print()
        