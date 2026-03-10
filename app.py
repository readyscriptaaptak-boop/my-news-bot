import streamlit as st
import feedparser
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

# हर 2 मिनट में ऑटो-रिफ्रेश (ताज़ा खबरों के लिए)
st_autorefresh(interval=120000, key="newsrefresh")

# IST टाइम सेट करना
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M:%S %p')

st.set_page_config(page_title="India Aaptak News - Live", page_icon="🚨", layout="wide")

# CSS: लुक को प्रोफेशनल बनाने के लिए
st.markdown("""
    <style>
    .header-style { background: #ce1212; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 5px; }
    .news-card { background: #1e1e1e; padding: 15px; border-radius: 8px; border-left: 5px solid #ce1212; margin-bottom: 15px; }
    .time-text { color: #ffbd45; text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-style"><h1>INDIA AAPTAK NEWS 🚨</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div class="time-text">Live Update (Jalgaon Time): {current_time}</div>', unsafe_allow_html=True)

# --- सर्च बॉक्स (User Input) ---
search_query = st.text_input("🔍 किसी खास विषय पर ताज़ा खबर खोजें (जैसे: Crime, Rain, Election)", "")

def get_latest_news(query):
    # 'when:12h' यह सुनिश्चित करता है कि सिर्फ पिछले 12 घंटे की खबर आए
    url = f"https://news.google.com/rss/search?q={query}+when:12h&hl=hi&gl=IN&ceid=IN:hi"
    feed = feedparser.parse(url)
    # खबरों को उनकी तारीख के हिसाब से सॉर्ट (Sort) करना ताकि सबसे नई ऊपर रहे
    entries = sorted(feed.entries, key=lambda x: x.published_parsed if hasattr(x, 'published_parsed') else 0, reverse=True)
    return entries[:12]

# --- टैब सिस्टम ---
tab1, tab2, tab3 = st.tabs(["📍 जलगाँव", "🚩 महाराष्ट्र", "🌍 देश-विदेश"])

with tab1:
    news_items = get_latest_news("Jalgaon")
    if not news_items:
        st.write("अभी जलगाँव की कोई नई खबर नहीं मिली।")
    for n in news_items:
        st.markdown(f'<div class="news-card"><h4>{n.title}</h4><p style="color:gray; font-size:12px;">Source: {n.source.title}</p></div>', unsafe_allow_html=True)
        st.link_button("पूरी खबर पढ़ें →", n.link)

with tab2:
    for n in get_latest_news("Maharashtra"):
        st.markdown(f'<div class="news-card"><h4>{n.title}</h4></div>', unsafe_allow_html=True)
        st.link_button("विवरण देखें →", n.link)

with tab3:
    # अगर यूजर ने सर्च बॉक्स में कुछ लिखा है तो वो दिखाओ, वरना Trending India News
    target_query = search_query if search_query else "India Trending"
    for n in get_latest_news(target_query):
        st.markdown(f'<div class="news-card"><h4>{n.title}</h4></div>', unsafe_allow_html=True)
        st.link_button("खबर पढ़ें →", n.link)

st.sidebar.title("India Aaptak Control")
st.sidebar.write(f"Last Auto-Sync: {current_time}")
if st.sidebar.button("🔄 अभी अपडेट करें"):
    st.rerun()
