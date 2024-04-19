# Newsletter Generator

<img src="newsletter.png" alt="newsletter" width="400"/>


## What you'll need

* Perplexity API Key (paid) - https://www.perplexity.ai/settings/api
* Serper API Key (has free tier) - https://serper.dev/

## Setup .env.local
- copy/rename `env.sample` to `.env.local` and populate with the API Keys
- you can choose another [Perplexity model](https://docs.perplexity.ai/docs/model-cards), if you want

## Dependencies

`pip install -r requirements.txt`

## Start the UI

`streamlit run startui.py`

Then open the UI on http://localhost:8501

## Input on the UI:
* System message (AI behaviour)
* Google search phrase
* Date the google news search should be run from

Based on the above criteria you'll get 10 generated articles that could be used for e.g.: a newsletter.

**The Generated Articles' format is**
* title
* source
* summary
* article highlights

Enjoy ✨