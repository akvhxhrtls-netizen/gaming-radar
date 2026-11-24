from datetime import datetime, timedelta, timezone
from collector import collect
from analyzer import summarize
from reporter import render

def main():
    from dotenv import load_dotenv
    load_dotenv()
    kst = timezone(timedelta(hours=9))
    end = datetime.now(kst).replace(hour=11,minute=0,second=0,microsecond=0)
    if end > datetime.now(kst):
        end -= timedelta(days=1)
    start = end-timedelta(days=1)
    rows, coverage = collect(start,end)
    print(render(start,end,summarize(rows),coverage,rows))

if __name__ == '__main__':
    main()
