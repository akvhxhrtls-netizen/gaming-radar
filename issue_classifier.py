import re
from collections import Counter


ISSUE_RULES = {
    "신작 및 출시": [
        "release", "launch", "trailer",
        "reveal", "announcement", "gameplay",
        "preorder", "release date"
    ],

    "업데이트": [
        "update", "patch", "dlc",
        "expansion", "hotfix", "balance",
        "new content"
    ],

    "소비자 불만 및 논란": [
        "bug", "bugs", "crash", "lag",
        "performance", "optimization",
        "controversy", "complaint",
        "backlash", "boycott", "debate",
        "pay to win", "microtransactions"
    ],

    "e스포츠": [
        "esports", "tournament",
        "championship", "roster",
        "transfer", "playoffs",
        "finals", "competitive"
    ],

    "산업 동향": [
        "ai", "artificial intelligence",
        "layoffs", "acquisition",
        "merger", "investment",
        "studio closure", "voice acting"
    ],

    "마케팅": [
        "marketing", "advertising",
        "campaign", "promotion",
        "collaboration", "sponsorship",
        "brand", "influencer"
    ],

    "소비자 구매 동향": [
        "sale", "discount", "price",
        "purchase", "wishlist",
        "recommendation", "deal",
        "recommendations", "buy"
    ],

    "커뮤니티 문화": [
        "meme", "memes", "fan art",
        "fanart", "cosplay", "community",
        "fan theory", "modding"
    ]
}


def classify_issue(title):

    text = title.lower()
    categories = []

    for category, keywords in ISSUE_RULES.items():

        matched = []

        for keyword in keywords:

            pattern = (
                r"\b"
                + re.escape(keyword)
                + r"\b"
            )

            if re.search(pattern, text):
                matched.append(keyword)

        if matched:

            categories.append({
                "category": category,
                "matched_keywords": matched
            })

    if not categories:

        categories.append({
            "category": "미분류",
            "matched_keywords": []
        })

    return categories


def classify_posts(rows):

    results = []
    seen_urls = set()

    for row in rows:

        if row["url"] in seen_urls:
            continue

        seen_urls.add(row["url"])

        results.append({
            **row,
            "categories": classify_issue(
                row["title"]
            )
        })

    return results


def summarize_categories(rows):

    counts = Counter()

    for row in rows:

        for item in row["categories"]:

            counts[item["category"]] += 1

    return counts.most_common()


if __name__ == "__main__":

    from database import load_posts

    rows = load_posts()
    results = classify_posts(rows)

    print("=== GAMING RADAR ISSUE CLASSIFIER ===")
    print("가상 데이터 기반 이슈 분류 테스트")
    print(f"분석 게시글: {len(results)}건")
    print()

    for rank, row in enumerate(results, 1):

        print(f"{rank}. {row['title']}")
        print(f"   커뮤니티: r/{row['subreddit']}")

        for item in row["categories"]:

            print(f"   분류: {item['category']}")

            print(
                "   판단 근거: "
                + (
                    ", ".join(item["matched_keywords"])
                    or "없음"
                )
            )

        print(f"   원문: {row['url']}")
        print()

    print("=== 이슈 유형별 게시글 수 ===")

    for category, count in summarize_categories(results):

        print(f"{category}: {count}건")

    print()
    print("※ 복수 분류 허용")
    print("※ 유형별 합계는 고유 게시글 수를 초과할 수 있음")
    print("※ 제목 기반 규칙 분류이며 추가 검토 필요")
    