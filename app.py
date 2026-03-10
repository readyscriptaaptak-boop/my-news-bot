import streamlit as st
import feedparser
import pytz
import trafilatura # पूरी खबर पढ़ने के लिए
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ऑटो-रिफ्रेश (10 मिनट)
st_autorefresh(interval=600000, key="news_studio")

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

st.set_page_config(page_title="India Aaptak AI Script Studio", page_icon="🎙️", layout="wide")

# प्रोफेशनल डार्क थीम डिजाइन
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #ce1212; color: white; border-radius: 8px; }
    .script-box { background-color: #161b22; padding: 25px; border-radius: 12px; border: 2px solid #ce1212; color: #e6edf3; font-size: 18px; line-height: 1.8; }
    .news-item { background: #1c2128; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- खबर के अंदर से जानकारी निकालने वाला फंक्शन ---
def get_full_article(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        text = trafilatura.extract(downloaded)
        return text if text else "खबर की पूरी जानकारी नहीं मिल पाई।"
    except:
        return "वेबसाइट से खबर पढ़ने में दिक्कत आ रही है।"

# --- न्यूज़ वॉइस-ओवर स्क्रिप्ट जनरेटर ---
def make_voiceover_script(title, full_text):
    # स्क्रिप्ट को प्रोफेशनल न्यूज़ फॉर्मेट में ढालना
    script = f"""
🎙️ **INDIA AAPTAK NEWS - VOICE OVER SCRIPT**
--------------------------------------------------
**(INTRO MUSIC - FAST & AGGRESSIVE)**

**एंकर (VO):** नमस्कार, आप देख रहे हैं इंडिया आपतक न्यूज़। इस वक्त की एक बड़ी खबर के साथ मैं हूँ आपका न्यूज़ एंकर।

**मुख्य समाचार:** {title}

**विस्तार से:** {full_text[:600]}... (आगे की जानकारी नीचे दी गई है)

**एंकर (VO):** जी हाँ, इस पूरे मामले ने अब तूल पकड़ लिया है। जो जानकारी हमारे पास आ रही है, उसके मुताबिक घटना के बाद से ही इलाके में सनसनी फैली हुई है। प्रशासन पूरी तरह अलर्ट पर है।

**क्लिप/विजुअल के लिए निर्देश:** (यहाँ घटना के विजुअल्स दिखाएं...)

**एंकर (VO):** इस खबर पर हम लगातार नज़र बनाए हुए हैं। आगे जो भी अपडेट आएगा, हम आप तक पहुँचाएंगे। देखते रहिए इंडिया आपतक न्यूज़। कैमरा पर्सन के साथ, मैं न्यूज़ डेस्क।
--------------------------------------------------
✅ **YouTube SEO:**
- **Title:** {title[:60]} | India Aaptak News
- **Hashtags:** #Jalgaon #BreakingNews #LatestUpdate
    """
    return script

st.title("🎙️ India Aaptak: AI Script Studio")
st.write(f"Digital Newsroom Live | {current_time}")

# न्यूज़ लोड करना
@st.cache_data(ttl=600)
def fetch_news(q):
    return feedparser.parse(f"https://news.google.com/rss/search?q={q}+when:24h&hl=hi&gl=IN&ceid=IN:hi").entries[:15]

col1, col2 = st.columns([1, 1.5])

with col1:
    st.header("📲 खबरें चुनें")
    category = st.selectbox("कैटेगरी", ["Jalgaon", "Maharashtra", "India"])
    news_list = fetch_news(category)
    
    for i, n in enumerate(news_list):
        st.markdown(f'<div class="news-item"><b>{n.title}</b></div>', unsafe_allow_html=True)
        if st.button(f"इस खबर को पढ़कर स्क्रिप्ट बनाएं ✨", key=f"btn_{i}"):
            st.session_state['url'] = n.link
            st.session_state['title'] = n.title

with col2:
    st.header("✍️ प्रोफेशनल स्क्रिप्ट")
    if 'url' in st.session_state:
        with st.spinner('रोबोट खबर पढ़ रहा है... कृपया इंतज़ार करें...'):
            # वेबसाइट पर जाकर खबर पढ़ना
            full_content = get_full_article(st.session_state['url'])
            # स्क्रिप्ट तैयार करना
            final_script = make_voiceover_script(st.session_state['title'], full_content)
            
            st.markdown(f'<div class="script-box">{final_script}</div>', unsafe_allow_html=True)
            
            # कॉपी करने के लिए टेक्स्ट एरिया
            st.text_area("स्क्रिप्ट कॉपी करें:", final_script, height=300)
    else:
        st.info("बाईं ओर से किसी भी खबर पर क्लिक करें। रोबोट उस वेबसाइट पर जाएगा और आपके लिए स्क्रिप्ट तैयार कर देगा।")

st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak AI: आपका रोबोट अब खबरें पढ़कर स्क्रिप्ट तैयार कर रहा है...</marquee></div>', unsafe_allow_html=True)
