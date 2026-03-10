import streamlit as st
import feedparser
from datetime import datetime
import pytz # टाइमज़ोन के लिए
from streamlit_autorefresh import st_autorefresh # ऑटो-रिफ्रेश के लिए

# हर 5 मिनट (300,000 milliseconds) में पेज अपने आप ताज़ा होगा
st_autorefresh(interval=300000, key="datarefresh")

# IST (Indian Standard Time) सेट करना
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M:%S %p')

st.set_page_config(page_title="India Aaptak News - LIVE", page_icon="🚨", layout="wide")

# डिजाइन
st.markdown("""
    <style>
    .header-box { background: #ff4b4b; padding: 20px; border-radius: 15px; color: white; text-align: center; }
    .update-time { font-size: 18px; color: #ffbd45; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .news-card { background: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>INDIA AAPTAK NEWS 🚨</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div class="update-time">Last Updated (IST): {current_time}</div>', unsafe_allow_html=True)

def load_news(query):
    url = f"https://news.google.com/rss/search?q={query}+when:24h&hl=hi&gl=IN&ceid=IN:hi"
    return feedparser.parse(url).entries[:12]

# टैब सिस्टम
tab1, tab2, tab3 = st.tabs(["📍 जलगाँव (Jalgaon)", "🚩 महाराष्ट्र", "🇮🇳 देश-विदेश"])

with tab1:
    for n in load_news("Jalgaon"):
        st.markdown(f'<div class="news-card"><h4>{n.title}</h4><p style="font-size:12px; color:gray;">Source: {n.source.title}</p></div>', unsafe_allow_html=True)
        st.link_button("पूरी खबर पढ़ें →", n.link)

with tab2:
    for n in load_news("Maharashtra"):
        st.info(f"**{n.title}**")
        st.link_button("Read More", n.link)

with tab3:
    for n in load_news("India Trending"):
        st.success(f"**{n.title}**")
        st.link_button("Read Details", n.link)

st.sidebar.info(f"रोबोट अभी एक्टिव है और जलगाँव की खबरें स्कैन कर रहा है।")
