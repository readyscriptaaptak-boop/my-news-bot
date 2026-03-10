import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import trafilatura
import pytz
from datetime import datetime
import time

# --- पेज सेटिंग ---
st.set_page_config(page_title="India Aaptak Master Studio", page_icon="🎙️", layout="wide")

# --- मेमोरी (State) ---
if 'final_script' not in st.session_state:
    st.session_state['final_script'] = ""

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

# --- स्टाइलिंग ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; }
    .main-header { background: linear-gradient(90deg, #ce1212, #8b0000); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px; }
    .script-box { background: #161b22; padding: 25px; border-radius: 12px; border-left: 8px solid #ffbd45; color: #f0f6fc; font-size: 18px; line-height: 1.8; }
    .news-card { background: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- असली 'Anti-Block' न्यूज़ रीडर ---
def smart_scrape(target_title):
    # 1. पहले इस टाइटल को गूगल पर फिर से सर्च करो ताकि 3-4 अलग लिंक मिलें
    search_url = f"https://news.google.com/rss/search?q={target_title}&hl=hi&gl=IN&ceid=IN:hi"
    search_feed = feedparser.parse(search_url)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
    # 2. टॉप 3 लिंक्स को एक-एक करके आज़माओ
    for entry in search_feed.entries[:3]:
        url = entry.link
        try:
            # Trafilatura से कोशिश
            downloaded = trafilatura.fetch_url(url)
            text = trafilatura.extract(downloaded)
            
            # अगर Trafilatura फेल हो, तो BeautifulSoup से कोशिश
            if not text or len(text) < 300:
                resp = requests.get(url, headers=headers, timeout=7)
                soup = BeautifulSoup(resp.content, 'html.parser')
                text = " ".join([p.text for p in soup.find_all('p') if len(p.text) > 40])
            
            if text and len(text) > 300:
                return text, entry.source.title # पक्की खबर मिल गई!
        except:
            continue
    return None, None

# --- स्क्रिप्ट मेकर ---
def generate_script(title, body, source):
    return f"""
🎙️ **INDIA AAPTAK NEWS: वॉइस-ओवर स्क्रिप्ट**
--------------------------------------------------
**(तेज़ म्यूजिक - INTRO)**

**एंकर (VO):** नमस्कार, आप देख रहे हैं 'इंडिया आपतक न्यूज़'। इस वक्त की बड़ी खबर जलगाँव से।

**हेडलाइन:** {title}

**खबर का विस्तार:** {body[:1200]}...

**एंकर (VO):** जी हाँ, **{source}** के अनुसार इस खबर ने अब पूरे इलाके में हलचल पैदा कर दी है। प्रशासन इस पर बारीकी से नज़र रखे हुए है। 

हर छोटी-बड़ी अपडेट के लिए 'इंडिया आपतक' को सब्सक्राइब करें। जय हिन्द!
--------------------------------------------------
✅ #Jalgaon #IndiaAaptak #BreakingNews
    """

st.markdown('<div class="main-header"><h1>INDIA AAPTAK AI STUDIO 🎙️</h1></div>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'><b>Status: Super-Sync Active ⚡ | {current_time}</b></p>", unsafe_allow_html=True)

# --- सर्च बार ---
s_query = st.text_input("🔍 कोई भी टॉपिक सर्च करें (जैसे: गुलाबराव पाटील, जळगाव पाऊस)", placeholder="Search here...")

c1, c2 = st.columns([1, 1.2])

with c1:
    st.subheader("📲 ताज़ा खबरें")
    base_topic = st.radio("कैटेगरी", ["Jalgaon", "Maharashtra", "India"], horizontal=True)
    final_q = s_query if s_query else base_topic
    
    feed = feedparser.parse(f"https://news.google.com/rss/search?q={final_q}+when:24h&hl=hi&gl=IN&ceid=IN:hi")
    
    for i, e in enumerate(feed.entries[:10]):
        with st.container():
            st.markdown(f'<div class="news-card"><b>{e.title}</b><br><small>{e.source.title}</small></div>', unsafe_allow_html=True)
            if st.button(f"इसकी स्क्रिप्ट बनाएं ✨", key=f"btn_{i}"):
                with st.spinner('रोबोट इंटरनेट खंगाल रहा है...'):
                    # अब यह फंक्शन उस खबर को 3 अलग सोर्सेज पर चेक करेगा
                    full_text, found_source = smart_scrape(e.title)
                    if full_text:
                        st.session_state['final_script'] = generate_script(e.title, full_text, found_source)
                    else:
                        st.error("माफी! यह खबर सभी जगह ब्लॉक है। कृपया कोई और खबर चुनें।")

with c2:
    st.subheader("✍️ आपकी रेडी-मेड स्क्रिप्ट")
    if st.session_state['final_script']:
        st.markdown(f'<div class="script-box">{st.session_state["final_script"]}</div>', unsafe_allow_html=True)
        st.text_area("कॉपी करें:", st.session_state['final_script'], height=450)
    else:
        st.info("बाईं ओर से खबर चुनें, रोबोट 'मल्टी-लिंक' सर्च करके स्क्रिप्ट तैयार कर देगा।")

st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak: अब हर खबर की स्क्रिप्ट मिलेगी, बिना किसी रुकावट के...</marquee></div>', unsafe_allow_html=True)
