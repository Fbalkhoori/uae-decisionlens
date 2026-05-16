import os
import requests
import feedparser
from datetime import datetime
from openai import OpenAI
from pytrends.request import TrendReq

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

current_date = datetime.now().strftime("%d/%m/%Y")

RSS_FEEDS = [
    "https://mediaoffice.ae/en/rss",
    "https://www.mediaoffice.abudhabi/en/rss/"
]

def fetch_news():
    if not NEWS_API_KEY:
        return "NewsAPI key not configured."

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "UAE OR Dubai OR Abu Dhabi AND AI OR economy OR climate OR cybersecurity OR education OR governance",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 8,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params, timeout=20)
    data = response.json()

    articles = data.get("articles", [])
    results = []

    for article in articles:
        results.append(
            f"- {article.get('title')} | {article.get('source', {}).get('name')}"
        )

    return "\n".join(results) if results else "No major NewsAPI signals found."


def fetch_google_trends():
    try:
        pytrends = TrendReq(hl="en-US", tz=240)
        keywords = ["UAE AI", "UAE economy", "Dubai technology", "UAE sustainability", "UAE cybersecurity"]
        pytrends.build_payload(keywords, timeframe="now 7-d", geo="AE")
        data = pytrends.interest_over_time()

        if data.empty:
            return "No major Google Trends signals found."

        latest = data.tail(1).to_dict("records")[0]
        return "\n".join([f"- {k}: {v}" for k, v in latest.items() if k != "isPartial"])

    except Exception as e:
        return f"Google Trends unavailable: {e}"


def fetch_rss():
    results = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:
            results.append(f"- {entry.get('title')}")

    return "\n".join(results) if results else "No UAE government RSS signals found."


def generate_brief():
    news_signals = fetch_news()
    trend_signals = fetch_google_trends()
    rss_signals = fetch_rss()

    prompt = f"""
You are UAE DecisionLens, an AI-powered sovereign decision intelligence and strategic foresight agent.

Date: {current_date}

You autonomously scanned public sources:
1. NewsAPI public news articles
2. Google Trends public search trend data
3. UAE government RSS feeds

NewsAPI signals:
{news_signals}

Google Trends signals:
{trend_signals}

UAE government RSS signals:
{rss_signals}

Task:
Detect emerging UAE-relevant strategic trends.
Generate 3 potential strategic or policy decisions for UAE leadership.
Then produce ONE executive Decision Impact Brief for the strongest decision.

The brief must include:
- Executive Summary
- Emerging Trend Detected
- Proposed Strategic Decision
- Strategic Alignment
- Opportunities
- Risks
- Stakeholder Impact
- Scenario Simulation
- Actionable Recommendations
- Final Conclusion

Use professional executive English.
Use minimal tables only if useful.
Do not include prepared by, signatures, or footer notes.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    report = response.choices[0].message.content

    filename = f"weekly_decisionlens_brief_{datetime.now().strftime('%Y%m%d')}.md"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)

    print("Weekly UAE DecisionLens brief generated successfully.")
    print(f"Saved file: {filename}")
    print(report)


if __name__ == "__main__":
    generate_brief()