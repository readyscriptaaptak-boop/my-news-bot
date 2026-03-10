import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Jalgaon Live News Robot", layout="wide")

# ऑटो रिफ्रेश (हर 5 मिनट में)
st.empty() 

st.title("🚨 LIVE TRENDING NEWS ROBOT")
st.write(f"Last Updated: {datetime.now().strftime('%H:%M:%S')}")

# सर्च फिल्टर
search_query = st.text_input("किसी खास टॉपिक पर न्यूज़ चाहिए? (जैसे: Crime, Rain)", "")

def get_news(query):
    url = f"https://news.google.com/rss/search?q={query}+when:24h&hl=hi&gl=IN&ceid=IN:hi"
    return feedparser.parse(url).entries[:10]

# श्रेणियाँ (Categories)
tabs = st.tabs(["📍 Jalgaon", "🚩 Maharashtra", "🇮🇳 India", "🔍 Search Results"])

with tabs[0]:
    for e in get_news("Jalgaon"):
        st.info(f"**{e.title}**")
        st.caption(f"Source: {e.source.title}")
        st.link_button("पूरी खबर पढ़ें", e.link)

with tabs[1]:
    for e in get_news("Maharashtra"):
        st.warning(f"**{e.title}**")
        st.link_button("Read More", e.link)

with tabs[2]:
    for e in get_news("India"):
        st.success(f"**{e.title}**")
        st.link_button("Read More", e.link)

with tabs[3]:
    if search_query:
        for e in get_news(search_query):
            st.error(f"**{e.title}**")
            st.link_button("Read More", e.link)
    else:
        st.write("सर्च करने के लिए ऊपर बॉक्स में टाइप करें।")
