from datetime import datetime, timedelta
import requests
import json
from dotenv import dotenv_values

config = dotenv_values(".env.local")


def get_news_urls(
    where="news", what="Most important AI and LLM related news this week", after=""
):
    url = f"https://google.serper.dev/{where}"

    if not after:
        now = datetime.now()
        a_week_ago = now - timedelta(days=7)
        formatted_a_week_ago = a_week_ago.strftime("%Y-%m-%d")
        after = formatted_a_week_ago

    payload = json.dumps(
        {
            "q": f"{what} after:{after}",
        }
    )
    headers = {
        "X-API-KEY": config["SERPER_API_KEY"],
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)


if __name__ == "__main__":
    for i in get_news_urls()["news"]:
        print(i["link"])
    print("Done!")
