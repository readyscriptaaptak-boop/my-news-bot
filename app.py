import streamlit as st
import feedparser
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# 1. हर 5 मिनट में ऑटो-रिफ्रेश (समय बढ़ा दिया है ताकि Google ब्लॉक न करे)
st_autorefresh(interval=300000, key="news_update")

# IST टाइम सेटअप
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M:%S %p')

st.set_page_config(page_title="India Aaptak News", page_icon="🚨", layout="wide")

# डिजाइन CSS
st.markdown("""
    <style>
    .header-box { background: #ce1212; padding: 15px; border-radius: 10px; color: white; text-align: center; }
    .news-card { background: #1e1e1e; padding: 15px; border-radius: 8px; border-left: 5px solid #ce1212; margin-bottom: 12px; }
    .time-style { color: #ffbd45; text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>INDIA AAPTAK NEWS 🚨</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div class="time-style">ताज़ा अपडेट (IST): {current_time}</div>', unsafe_allow_html=True)

# --- न्यूज़ फेच करने वाला फंक्शन (Cache के साथ ताकि Error न आए) ---
@st.cache_data(ttl=600) # 10 मिनट तक न्यूज़ को याद रखेगा
def fetch_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={query}+when:24h&hl=hi&gl=IN&ceid=IN:hi"
        feed = feedparser.parse(url)
        if feed.entries:
            # तारीख के हिसाब से सबसे ताज़ा खबर ऊपर
            return sorted(feed.entries, key=lambda x: x.published_parsed if hasattr(x, 'published_parsed') else 0, reverse=True)[:12]
        else:
            return []
    except Exception as e:
        return []

# --- सर्च बॉक्स ---
search_query = st.text_input("🔍 यहाँ सर्च करें (उदा: Accident, Crime, Weather)", "")

# --- टैब सिस्टम ---
tab1, tab2, tab3 = st.tabs(["📍 जलगाँव", "🚩 महाराष्ट्र", "🌍 देश-विदेश"])

def display_news(news_list):
    if not news_list:
        st.warning("फिलहाल कोई ताज़ा खबर नहीं मिली। कृपया थोड़ी देर बाद देखें।")
    else:
        for n in news_list:
            source = getattr(n, 'source', {'title': 'News Agency'}).title
            st.markdown(f'<div class="news-card"><h4>{n.title}</h4><p style="color:gray; font-size:12px;">सोर्स: {source}</p></div>', unsafe_allow_html=True)
            st.link_button("पूरी खबर पढ़ें →", n.link)

with tab1:
    display_news(fetch_news("Jalgaon"))

with tab2:
    display_news(fetch_news("Maharashtra"))

with tab3:
    q = search_query if search_query else "India Breaking"
    display_news(fetch_news(q))

st.sidebar.title("News Robot Status")
st.sidebar.success("Robot is Online ✅")
st.sidebar.write(f"Last Sync: {current_time}")
if st.sidebar.button("🔄 Force Refresh"):
    st.cache_data.clear()
    st.rerun()
