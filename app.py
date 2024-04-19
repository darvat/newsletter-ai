import requests
from pprint import pprint
from serper_news import get_news_urls
from dotenv import dotenv_values

config = dotenv_values(".env.local")


def format_to_markdown(data):
    markdown_output = f"## {data['title']}\n\n"
    markdown_output += f"**Source**: [{data['source']}]({data['url']})\n\n"
    markdown_output += f"**Summary**: {data['snippet']}\n\n"
    markdown_output += f"### Article highlights\n\n"
    markdown_output += data["message_content"]

    return markdown_output


def main(
    system_message="""
        You are a renowned AI expert and you write a weekly AI newsletter. 
        You need to summarize the most important AI news of given input.
        """,
    where="news",
    what="Most important AI and LLM related news this week",
    after="",
):
    for news in get_news_urls(where, what, after)["news"]:

        news_url = news["link"]

        # print(f"Processing news from: {news_url}")

        payload = {
            "model": f"{config['PPLX_MODEL']}",
            "messages": [
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": news_url,
                },
            ],
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {config['PPLX_API_KEY']}",
        }

        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                json=payload,
                headers=headers,
            )

            data = response.json()

            message_content = data["choices"][0]["message"]["content"]
            news_info = {
                "url": news_url,
                "message_content": message_content,
                "title": news["title"],
                "snippet": news["snippet"],
                "source": news["source"],
            }
            yield {"title": news["title"], "data": format_to_markdown(news_info)}
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            continue
        except KeyError as e:
            print(f"Error accessing data: {e}")
            continue


if __name__ == "__main__":
    pprint(main())
