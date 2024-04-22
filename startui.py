from time import sleep
import streamlit as st
from datetime import datetime, timedelta
from textwrap import dedent
from app import main as gen_main

st.set_page_config(
    page_title="Newsletter Generator App",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.title("Newsletter Generator App")
st.write(
    """
    This app generates content that can be used e.g., for a newsletter by summarizing the most important news, search hits.
    """
)

if "running" not in st.session_state:
    st.session_state.running = False

if "generated_news" not in st.session_state:
    st.session_state.generated_news = []

if "just_completed" not in st.session_state:
    st.session_state.just_completed = False

if not st.session_state.running and not st.session_state.generated_news:
    st.image("newsletter.png", width=800)


system_message = st.sidebar.text_area(
    "🤖 AI behaviour: Tell the system how it should act and behave.",
    dedent(
        """
        You are a renowned AI expert and you write a weekly AI newsletter. 
        You need to summarize the most important AI news of the given inputs.
        """
    ).strip(),
    height=200,
    key="system_message",
    max_chars=200,
)

where = st.sidebar.selectbox(
    "🔎 Search in (disabled for now)",
    [
        "news",
        "search",
    ],
    key="where",
    disabled=True,
)
what = st.sidebar.text_area(
    "❓Google search phrase",
    "Most important AI and LLM related news this week",
    key="what",
    max_chars=128,
)

after = st.sidebar.date_input(
    "📆 Search after",
    value=datetime.now() - timedelta(7),
    max_value=datetime.now(),
    key="after",
)
after = after.strftime("%Y-%m-%d")

col1, col2 = st.sidebar.columns(2)

placeholder = st.empty()
placeholder_container = placeholder.container()


def genbuttonclick():
    st.session_state.running = True
    st.session_state.generated_news = []
    st.session_state.just_completed = False
    placeholder.empty()
    sleep(0.1)


with col1:
    st.button(
        "Generate ✨",
        use_container_width=True,
        disabled=st.session_state.running,
        on_click=genbuttonclick,
    )

with col2:
    st.button(
        "Stop ❌",
        disabled=not st.session_state.running,
        use_container_width=True,
        on_click=lambda: setattr(st.session_state, "running", False),
    )


with placeholder_container:
    if st.session_state.running:
        with st.spinner("Generating newsletter... Please wait."):
            result_generator = gen_main(system_message, where, what, after)
            for news in result_generator:
                st.session_state.generated_news.append(news)
                if not st.session_state.running:
                    break
                with st.expander(news["title"]):
                    st.markdown(news["data"])
            st.session_state.running = False
            st.session_state.just_completed = True
    elif len(st.session_state.generated_news) > 0:
        for news in st.session_state.generated_news:
            with st.expander(news["title"]):
                st.markdown(news["data"])


if (
    not st.session_state.running
    and st.session_state.generated_news
    and st.session_state.just_completed
):
    st.session_state.just_completed = False  # Reset the flag
    st.rerun()
