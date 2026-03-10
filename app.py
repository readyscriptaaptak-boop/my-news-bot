import streamlit as st
import feedparser
import pytz
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ऑटो-रिफ्रेश (3 मिनट)
st_autorefresh(interval=180000, key="studio_update")

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

st.set_page_config(page_title="India Aaptak - News Studio", page_icon="🎙️", layout="wide")

# CSS: प्रोफेशनल लुक के लिए
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; background-color: #ce1212; color: white; }
    .script-box { background-color: #0e1117; padding: 20px; border: 2px solid #ffbd45; border-radius: 10px; color: #ffffff; }
    .news-card { background: #1e1e1e; padding: 15px; border-radius: 10px; border-left: 5px solid #ffbd45; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🎙️ India Aaptak: News Studio")
st.write(f"Digital Anchor System | {current_time}")

# --- स्क्रिप्ट जनरेटर फंक्शन (Recreation Logic) ---
def recreate_script(title):
    # यह न्यूज़ हेडलाइन को एंकर स्क्रिप्ट के फॉर्मेट में बदलता है
    script = f"""
🎤 **न्यूज़ एंकर स्क्रिप्ट (Voice-over):**
--------------------------------------------------
(Intro म्यूजिक...)
नमस्कार, आप देख रहे हैं 'इंडिया आपतक न्यूज़'। मैं हूँ आपका डिजिटल एंकर।

आज की बड़ी खबर: **{title}**

इस वक्त की जो जानकारी निकलकर सामने आ रही है, उसके मुताबिक घटना काफी गंभीर है। हमारे सूत्र बता रहे हैं कि स्थानीय प्रशासन मौके पर मौजूद है और मामले की पूरी जांच की जा रही है। 

(Anchor Note: यहाँ खबर की और डिटेल्स जोड़ें...)

इस खबर पर हमारी नज़र बनी हुई है। ताज़ा अपडेट्स के लिए बने रहें हमारे साथ।
--------------------------------------------------
✅ **YouTube SEO (TTD Mode):**
- **Title:** {title} | Breaking News | India Aaptak
- **Hashtags:** #JalgaonNews #BreakingNews #IndiaAaptak #Trending
    """
    return script

# --- न्यूज़ फेचिंग इंजन ---
@st.cache_data(ttl=300)
def fetch_mega_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={query}+when:12h&hl=hi&gl=IN&ceid=IN:hi"
        feed = feedparser.parse(url)
        return feed.entries[:15]
    except:
        return []

# --- मुख्य लेआउट (Two Columns) ---
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🌐 लाइव न्यूज़ फीड")
    category = st.selectbox("कैटेगरी चुनें", ["Jalgaon", "Maharashtra", "India"])
    news_data = fetch_mega_news(category)
    
    for i, n in enumerate(news_data):
        with st.container():
            st.markdown(f'<div class="news-card"><b>{n.title}</b><br><small>{n.source.title}</small></div>', unsafe_allow_html=True)
            # बटन जो स्क्रिप्ट जनरेट करेगा
            if st.button(f"इस खबर की स्क्रिप्ट बनाएं ✍️", key=f"btn_{i}"):
                st.session_state['selected_title'] = n.title

with col2:
    st.header("📝 न्यूज़ राइटिंग स्टूडियो")
    if 'selected_title' in st.session_state:
        st.success(f"चुनी गई खबर: {st.session_state['selected_title']}")
        
        # स्क्रिप्ट रीक्रिएशन एरिया
        final_script = recreate_script(st.session_state['selected_title'])
        st.markdown(f'<div class="script-box">{final_script}</div>', unsafe_allow_html=True)
        
        # WhatsApp शेयर मैसेज
        wa_msg = f"🚨 *ब्रेकिंग न्यूज़: इंडिया आपतक* 🚨\n\n{st.session_state['selected_title']}\n\nपूरी खबर के लिए यहाँ क्लिक करें: [Link]"
        st.text_area("WhatsApp के लिए कॉपी करें:", wa_msg)
    else:
        st.info("बाईं ओर से किसी खबर पर 'स्क्रिप्ट बनाएं' बटन दबाएं।")

# नीचे चलने वाली न्यूज़ पट्टी
st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak Studio: खबरें चुनें और तुरंत स्क्रिप्ट तैयार करें...</marquee></div>', unsafe_allow_html=True)
