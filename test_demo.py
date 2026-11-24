from datetime import datetime, timedelta, timezone
from analyzer import summarize
from reporter import render

kst = timezone(timedelta(hours=9))
end = datetime.now(kst).replace(
    hour=11, minute=0, second=0, microsecond=0
)
if end > datetime.now(kst):
    end -= timedelta(days=1)
start = end - timedelta(days=1)

# Synthetic test data only
topics = [
    ("gaming", "GTA 6 trailer discussion", 1200, 340),
    ("Games", "GTA 6 release expectations", 950, 210),
    ("pcgaming", "GTA 6 PC performance concerns", 720, 180),
    ("Steam", "Steam winter sale recommendations", 540, 120),
    ("pcgaming", "Steam winter sale wishlist", 430, 95),
    ("esports", "Valorant esports tournament discussion", 810, 240),
    ("ValorantCompetitive", "Valorant roster changes", 650, 170),
    ("leagueoflegends", "League of Legends esports season", 900, 260),
    ("IndieGaming", "Indie game marketing strategies", 320, 85),
    ("gamedev", "Indie game marketing on social media", 280, 70),
]

rows = []

for i, (subreddit, title, score, comments) in enumerate(topics):
    rows.append({
        "subreddit": subreddit,
        "title": title,
        "score": score,
        "comments": comments,
        "created": (end - timedelta(hours=i+1)).isoformat(),
        "url": f"https://example.com/demo/{i+1}"
    })

coverage = {
    row["subreddit"]: "가상 데이터"
    for row in rows
}

stats = summarize(rows)

print("=== SYNTHETIC DATA TEST ===")
print(render(start, end, stats, coverage, rows))
from database import save_posts, load_posts

save_posts(rows)

stored_rows = load_posts()

print("\n=== DATABASE TEST ===")
print(f"저장된 게시글: {len(stored_rows)}건")
print("데이터베이스 저장 완료")