import streamlit as st
import feedparser
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# हर 3 मिनट में ऑटो-अपडेट
st_autorefresh(interval=180000, key="news_bazar_update")

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

st.set_page_config(page_title="India Aaptak - Khabron Ka Bazar", page_icon="🔥", layout="wide")

# प्रोफेशनल न्यूज़ लुक (Dark Theme + Red Accents)
st.markdown("""
    <style>
    .main-title { background: #ce1212; padding: 15px; border-radius: 10px; color: white; text-align: center; font-size: 35px; font-weight: bold; }
    .news-card { background: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 6px solid #ffbd45; margin-bottom: 15px; transition: 0.3s; }
    .news-card:hover { border-left: 6px solid #ce1212; background: #252525; }
    .trending-tag { background: #ff4b4b; color: white; padding: 2px 8px; border-radius: 5px; font-size: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">INDIA AAPTAK: खबरों का बाज़ार 🔥</div>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'><b>Last Sync: {current_time} (IST)</b></p>", unsafe_allow_html=True)

# --- ताक़तवर न्यूज़ इंजन (Multi-Source Search) ---
@st.cache_data(ttl=300) # 5 मिनट का कैश ताकि एरर न आए
def fetch_mega_news(category_type):
    all_entries = []
    
    # कैटेगरी के हिसाब से अलग-अलग सर्च क्वेरीज़
    queries = {
        "INDIA": ["India+Breaking+News", "India+Trending", "Viral+News+India", "Latest+India+News"],
        "MAHARASHTRA": ["Maharashtra+Breaking", "Marathi+News+Latest", "Maharashtra+Politics"],
        "JALGAON": ["Jalgaon+News+Today", "जळगाव+ताज्या+बातमी", "Jalgaon+Crime+News"]
    }
    
    search_list = queries.get(category_type, ["India"])
    
    for q in search_list:
        try:
            url = f"https://news.google.com/rss/search?q={q}+when:12h&hl=hi&gl=IN&ceid=IN:hi"
            feed = feedparser.parse(url)
            all_entries.extend(feed.entries)
        except:
            continue
            
    # डुप्लीकेट खबरें हटाना (Link के आधार पर)
    seen_links = set()
    unique_news = []
    for entry in all_entries:
        if entry.link not in seen_links:
            unique_news.append(entry)
            seen_links.add(entry.link)
            
    # सबसे नई खबर सबसे ऊपर (Sorting)
    unique_news = sorted(unique_news, key=lambda x: x.published_parsed if hasattr(x, 'published_parsed') else 0, reverse=True)
    return unique_news[:30] # हर सेक्शन में 30 टॉप खबरें

# --- सर्च बार ---
user_search = st.text_input("🔍 पूरे इंटरनेट पर कुछ भी खोजें (उदा: Cricket, Gold Rate, Modi)", "")

# --- मुख्य स्क्रीन ---
tab1, tab2, tab3 = st.tabs(["🔥 ताज़ा भारत (India)", "🚩 महाराष्ट्र", "📍 जलगाँव"])

def show_news(data):
    if not data:
        st.error("फिलहाल खबरें लोड नहीं हो पा रही हैं। रिफ्रेश करें।")
    else:
        for n in data:
            with st.container():
                st.markdown(f"""
                <div class="news-card">
                    <span class="trending-tag">TRENDING</span>
                    <h3 style="margin:10px 0; font-size:18px;">{n.title}</h3>
                    <p style="color:#888; font-size:12px;">सोर्स: {getattr(n, 'source', {'title': 'Breaking News'}).title}</p>
                </div>
                """, unsafe_allow_html=True)
                st.link_button("पूरी खबर पढ़ें 🔗", n.link)

with tab1:
    if user_search:
        st.subheader(f"सर्च रिजल्ट: {user_search}")
        show_news(fetch_mega_news(user_search)) # कस्टम सर्च
    else:
        show_news(fetch_mega_news("INDIA"))

with tab2:
    show_news(fetch_mega_news("MAHARASHTRA"))

with tab3:
    show_news(fetch_mega_news("JALGAON"))

# --- नीचे चलने वाली न्यूज़ पट्टी (Ticker) ---
st.markdown("""
    <div style="position: fixed; bottom: 0; left: 0; width: 100%; background: #ce1212; color: white; padding: 5px; font-weight: bold; z-index: 999;">
        <marquee>India Aaptak News Robot: जलगाँव, महाराष्ट्र और देश की हर ताज़ा खबर यहाँ उपलब्ध है... 24/7 लाइव अपडेट...</marquee>
    </div>
""", unsafe_allow_html=True)
