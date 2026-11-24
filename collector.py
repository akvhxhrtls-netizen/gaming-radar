import os
from datetime import datetime, timezone

SUBREDDITS = 'gaming Games pcgaming Steam gamedev esports IndieGaming truegaming PS5 XboxSeriesX NintendoSwitch leagueoflegends ValorantCompetitive GlobalOffensive DotA2 MMORPG gachagaming IndieDev GameDeals pcmasterrace'.split()

def collect(start, end):
    if os.getenv('REDDIT_ACCESS_APPROVED') != 'yes':
        raise RuntimeError('Obtain explicit Reddit approval before collecting data.')
    import praw
    reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'], client_secret=os.environ['REDDIT_CLIENT_SECRET'], user_agent=os.environ['REDDIT_USER_AGENT'])
    rows, coverage = {}, {}
    for name in SUBREDDITS:
        coverage[name] = 'partial: listing limit or time boundary not verified'
        try:
            for p in reddit.subreddit(name).new(limit=1000):
                created = datetime.fromtimestamp(p.created_utc, timezone.utc)
                if created < start:
                    coverage[name] = 'reached start boundary; not guaranteed exhaustive'
                    break
                if created >= end or p.removed_by_category or p.selftext in ('[deleted]', '[removed]'):
                    continue
                rows[p.id] = dict(id=p.id, subreddit=name, title=p.title, body=p.selftext, created=created.isoformat(), score=p.score, comments=p.num_comments, url='https://www.reddit.com'+p.permalink, crosspost=getattr(p,'crosspost_parent',None))
        except Exception as e:
            coverage[name] = 'access incomplete: '+type(e).__name__
    return list(rows.values()), coverage

def sample_comments(reddit, post_id, limit=10):
    # Optional, only if approved; no author identifiers retained.
    post = reddit.submission(id=post_id)
    post.comment_sort = 'top'
    post.comments.replace_more(limit=0)
    return [dict(body=c.body, score=c.score, url='https://www.reddit.com'+c.permalink) for c in post.comments[:limit] if c.body not in ('[deleted]','[removed]')]
