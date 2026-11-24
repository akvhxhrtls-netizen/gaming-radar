import re
from collections import Counter

# Candidate discovery, not a semantic classifier. Human review required.
STOP = set('the a an and or to of in on for is it my i you this that with how what why are was be game games gaming new just from at as do does can have has'.split())
def candidates(rows, limit=30):
    counts = Counter()
    for row in rows:
        words = re.findall(r"[a-z][a-z0-9'-]{2,}", row['title'].lower())
        counts.update(set(w for w in words if w not in STOP))
    return counts.most_common(limit)

def summarize(rows, previous=None):
    # Counts represent observed unique posts, not total Reddit volume.
    return {'observed':len(rows), 'communities':dict(Counter(r['subreddit'] for r in rows)), 'candidates':candidates(rows), 'growth':None}
