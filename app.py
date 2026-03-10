import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import trafilatura
import pytz
from datetime import datetime
from urllib.parse import quote # URL की गड़बड़ी ठीक करने के लिए

# --- पेज सेटिंग ---
st.set_page_config(page_title="India Aaptak AI Studio", page_icon="🎙️", layout="wide")

# --- मेमोरी (State) ---
if 'final_script' not in st.session_state:
    st.session_state['final_script'] = ""

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

# --- स्टाइलिंग ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .main-header { background: linear-gradient(90deg, #ce1212, #8b0000); padding: 20px; border-radius: 15px; color: white; text-align: center; }
    .script-box { background: #161b22; padding: 25px; border-radius: 12px; border-left: 8px solid #ffbd45; color: #f0f6fc; font-size: 19px; line-height: 1.8; }
    .news-card { background: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- असली 'Anti-Block' न्यूज़ रीडर ---
def smart_scrape(target_title):
    # URL Encoding: यहाँ हमने quote(target_title) जोड़ दिया है ताकि Error न आए
    encoded_title = quote(target_title)
    search_url = f"https://news.google.com/rss/search?q={encoded_title}&hl=hi&gl=IN&ceid=IN:hi"
    
    search_feed = feedparser.parse(search_url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
    # टॉप 3 लिंक्स को चेक करना
    for entry in search_feed.entries[:3]:
        url = entry.link
        try:
            downloaded = trafilatura.fetch_url(url)
            text = trafilatura.extract(downloaded)
            
            if not text or len(text) < 300:
                resp = requests.get(url, headers=headers, timeout=7)
                soup = BeautifulSoup(resp.content, 'html.parser')
                text = " ".join([p.text for p in soup.find_all('p') if len(p.text) > 40])
            
            if text and len(text) > 300:
                return text, entry.source.title 
        except:
            continue
    return None, None

# --- स्क्रिप्ट मेकर ---
def generate_script(title, body, source):
    return f"""
🎙️ **INDIA AAPTAK NEWS: प्रॉपर वॉइस-ओवर स्क्रिप्ट**
--------------------------------------------------
**(तेज़ न्यूज़ म्यूजिक - INTRO)**

**एंकर (VO):** नमस्कार, आप देख रहे हैं 'इंडिया आपतक न्यूज़'। जलगाँव और महाराष्ट्र की इस वक्त की सबसे बड़ी खबर के साथ मैं हूँ आपका न्यूज़ डेस्क।

**हेडलाइन:** {title}

**खबर का विस्तार:** {body[:1500]}

**(गंभीर स्वर में)**
**एंकर (VO):** जी हाँ, दर्शकों... जैसा कि आपने सुना, **{source}** के अनुसार यह मामला अब काफी गंभीर होता जा रहा है। हमारे सूत्रों के मुताबिक, प्रशासन इस पर पैनी नज़र बनाए हुए है और जल्द ही कुछ और बड़े खुलासे होने की उम्मीद है।

ताज़ा अपडेट्स और सटीक जानकारी के लिए बने रहें 'इंडिया आपतक न्यूज़' के साथ। 

**(आउटरो म्यूजिक)**
**एंकर (VO):** कैमरा पर्सन के साथ, मैं न्यूज़ डेस्क। जय हिन्द!
--------------------------------------------------
✅ #Jalgaon #IndiaAaptak #BreakingNews
    """

st.markdown('<div class="main-header"><h1>INDIA AAPTAK AI STUDIO 🎙️</h1></div>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'><b>Status: Connected ⚡ | {current_time}</b></p>", unsafe_allow_html=True)

# --- सर्च बार ---
s_query = st.text_input("🔍 कोई भी टॉपिक सर्च करें", placeholder="यहाँ टाइप करें...")

c1, c2 = st.columns([1, 1.3])

with c1:
    st.subheader("📲 ताज़ा खबरें")
    base_topic = st.radio("कैटेगरी", ["Jalgaon", "Maharashtra", "India"], horizontal=True)
    final_q = s_query if s_query else base_topic
    
    # यहाँ भी URL सुरक्षित करने के लिए quote का उपयोग किया है
    main_feed_url = f"https://news.google.com/rss/search?q={quote(final_q)}+when:24h&hl=hi&gl=IN&ceid=IN:hi"
    feed = feedparser.parse(main_feed_url)
    
    for i, e in enumerate(feed.entries[:12]):
        with st.container():
            st.markdown(f'<div class="news-card"><b>{e.title}</b><br><small>{e.source.title}</small></div>', unsafe_allow_html=True)
            if st.button(f"इसकी पूरी स्क्रिप्ट बनाएं ✨", key=f"btn_{i}"):
                with st.spinner('रोबोट इंटरनेट से जानकारी निकाल रहा है...'):
                    full_text, found_source = smart_scrape(e.title)
                    if full_text:
                        st.session_state['final_script'] = generate_script(e.title, full_text, found_source)
                    else:
                        st.error("माफी! इस खबर की डिटेल किसी भी पोर्टल पर नहीं मिल पाई।")

with c2:
    st.subheader("✍️ आपकी रेडी-मेड स्क्रिप्ट")
    if st.session_state['final_script']:
        st.markdown(f'<div class="script-box">{st.session_state["final_script"]}</div>', unsafe_allow_html=True)
        st.text_area("कॉपी करें:", st.session_state['final_script'], height=500)
    else:
        st.info("👈 बाईं ओर से न्यूज़ चुनें, रोबोट 'मल्टी-लिंक' सर्च करके पूरी स्क्रिप्ट लिख देगा।")

st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak AI: अब हर खबर की पूरी स्क्रिप्ट मिलेगी... बिना किसी रुकावट के...</marquee></div>', unsafe_allow_html=True)
