# Gaming Radar

A proposed personal, non-commercial gaming community monitoring project for Korean-language learning and professional development. This repository is a prototype for Reddit's review, not an approved or deployed service.

## Proposed workflow
Read-only collection from 20 gaming subreddits; unique post IDs, timestamps, titles, public text, scores, comment counts and source links; topic classification, daily volume comparison, balanced discussion summaries and private email delivery at 11 AM KST. No posting, voting, messaging, moderation, profiling or model training.

## Current implementation
PRAW listing collection, time-window filtering, ID deduplication, per-community coverage flags, title keyword candidates and Korean review-draft output. An optional comment sampling helper is provided but not invoked by default. Keyword candidates are not validated central-topic counts. Crossposts are separate posts with parent IDs retained. Listings may be incomplete. Scores are not gross upvote totals.

## Not yet implemented
Semantic topic grouping, verified daily comparisons, AI-assisted summaries, persistent storage with deletion synchronization, external fact checking, scheduled execution and email integration. These require additional development and approval of the relevant data processing. No external AI service receives Reddit data in this prototype.

## Setup (only after explicit Reddit approval)
1. Install Python 3.10+ and run `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env` locally. Configure approved OAuth credentials and descriptive user agent. Never commit secrets.
3. Set `REDDIT_ACCESS_APPROVED=yes` only after approval and only if the approved scope matches this implementation.
4. Run `python main.py` to print a draft for the most recent completed 11 AM KST window. Do not publish or persist output unless permitted.

See PRIVACY.md. The requested scope and Devvit suitability are subject to Reddit's guidance. The prototype has not been tested against the live API.
