from discovery import discover_topics


def is_related(first, second):

    first_words = first["topic"].split()
    second_words = second["topic"].split()

    first_links = set(first["links"])
    second_links = set(second["links"])

    if first_links != second_links:
        return False

    short, long = sorted(
        [first_words, second_words],
        key=len
    )

    return any(
        long[i:i + len(short)] == short
        for i in range(len(long) - len(short) + 1)
    )


def merge_topics(candidates):

    ordered = sorted(
        candidates,
        key=lambda x: (
            len(x["topic"].split()),
            x["posts"],
            x["topic"]
        ),
        reverse=True
    )

    merged = []

    for candidate in ordered:

        matched = False

        for existing in merged:

            if is_related(existing, candidate):

                existing["aliases"].append(
                    candidate["topic"]
                )

                matched = True
                break

        if not matched:

            merged.append({
                **candidate,
                "aliases": []
            })

    merged.sort(
        key=lambda x: (
            x["posts"],
            len(x["communities"]),
            x["comments"]
        ),
        reverse=True
    )

    return merged


if __name__ == "__main__":

    # 실제 Reddit 데이터가 아닌 가상 데이터

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

    candidates = discover_topics(rows)
    results = merge_topics(candidates)

    print("=== GAMING RADAR TOPIC MERGER ===")
    print("가상 데이터 기반 주제 통합 테스트")
    print(f"통합 전 후보: {len(candidates)}개")
    print(f"통합 후 후보: {len(results)}개")
    print()

    for rank, data in enumerate(results, 1):

        print(f"{rank}. {data['topic']}")
        print(f"   게시글 수: {data['posts']}건")
        print(f"   총 점수: {data['score']:,}")
        print(f"   총 댓글 수: {data['comments']:,}")

        print(
            "   통합된 키워드: "
            + (", ".join(data["aliases"]) or "없음")
        )

        print(
            "   관련 커뮤니티: "
            + ", ".join(data["communities"])
        )

        print("   관련 링크:")

        for link in data["links"]:
            print(f"   - {link}")

        print()
        