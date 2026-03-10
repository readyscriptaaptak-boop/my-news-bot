import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import trafilatura
import pytz
from datetime import datetime

# --- पेज सेटिंग ---
st.set_page_config(page_title="India Aaptak AI Newsroom", page_icon="🎙️", layout="wide")

# --- मेमोरी सेटअप ---
if 'script_output' not in st.session_state:
    st.session_state['script_output'] = ""

IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

# --- ब्लॉक की गई साइट्स से खबर निकालने वाला 'मास्टर' फंक्शन ---
def fetch_unblocked_news(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    try:
        # तरीका 1: Trafilatura (फास्ट)
        downloaded = trafilatura.fetch_url(url)
        content = trafilatura.extract(downloaded)
        
        # तरीका 2: अगर तरीका 1 फेल हो जाए (Manual Scraping)
        if not content or len(content) < 200:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            # वेबसाइट के सभी पैराग्राफ्स (<p> tags) को उठाना
            paragraphs = soup.find_all('p')
            content = " ".join([p.text for p in paragraphs if len(p.text) > 50])
            
        return content if content and len(content) > 100 else None
    except:
        return None

# --- वॉइस-ओवर स्क्रिप्ट जनरेटर ---
def create_script(title, raw_text):
    full_script = f"""
🎙️ **INDIA AAPTAK NEWS: प्रॉपर वॉइस ओवर स्क्रिप्ट**
--------------------------------------------------
**(तेज़ न्यूज़ म्यूजिक - INTRO)**

**एंकर (VO):** नमस्कार, आप देख रहे हैं 'इंडिया आपतक न्यूज़'। जलगाँव और महाराष्ट्र की इस वक्त की सबसे बड़ी खबर के साथ मैं हूँ आपका न्यूज़ डेस्क।

**बड़ी खबर:** {title}

**विस्तार से:** {raw_text[:1500]} 

**(गंभीर स्वर में)**
**एंकर (VO):** जी हाँ, इस पूरे मामले ने अब तूल पकड़ लिया है। जलगाँव से लेकर मुंबई तक इस खबर की चर्चा है। प्रशासन इस पर पैनी नज़र बनाए हुए है और आने वाले समय में कुछ और बड़े खुलासे होने की उम्मीद है। 

हर ताज़ा अपडेट के लिए बने रहें 'इंडिया आपतक न्यूज़' के साथ। 

**(आउटरो म्यूजिक)**
**एंकर (VO):** कैमरा पर्सन के साथ, मैं न्यूज़ डेस्क। जय हिन्द!
--------------------------------------------------
✅ **YouTube SEO:**
- **Title:** {title[:70]}
- **Tags:** #JalgaonNews #IndiaAaptak #LatestUpdate
    """
    return full_script

# --- UI Layout ---
st.markdown("<h1 style='text-align: center; color: #ce1212;'>🎙️ INDIA AAPTAK NEWS STUDIO</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'><b>IST: {current_time} | Status: Online ✅</b></p>", unsafe_allow_html=True)

search_val = st.text_input("🔍 खबर खोजें (उदा: गुलाबराव पाटील, जळगाव पाऊस)", placeholder="यहाँ टाइप करें...")

c1, c2 = st.columns([1, 1.2])

with c1:
    st.subheader("📲 ताज़ा खबरें")
    topic = st.radio("कैटेगरी", ["Jalgaon", "Maharashtra", "India"], horizontal=True)
    q = search_val if search_val else topic
    
    feed = feedparser.parse(f"https://news.google.com/rss/search?q={q}+when:24h&hl=hi&gl=IN&ceid=IN:hi")
    
    for i, entry in enumerate(feed.entries[:12]):
        with st.container():
            st.markdown(f'<div style="background:#1e1e1e; padding:10px; border-radius:5px; margin-bottom:5px;"><b>{entry.title}</b></div>', unsafe_allow_html=True)
            if st.button(f"पूरी स्क्रिप्ट तैयार करें ✨", key=f"btn_{i}"):
                with st.spinner('रोबोट खबर पढ़ रहा है...'):
                    news_body = fetch_unblocked_news(entry.link)
                    if news_body:
                        st.session_state['script_output'] = create_script(entry.title, news_body)
                    else:
                        st.error("यह न्यूज़ साइट बहुत ज़्यादा सुरक्षित है, कृपया दूसरी न्यूज़ ट्राई करें।")

with c2:
    st.subheader("✍️ फाइनल न्यूज़ स्क्रिप्ट")
    if st.session_state['script_output']:
        st.markdown(f'<div style="background:#111; padding:20px; border-radius:10px; border-left:8px solid #ce1212; color:white; font-size:18px;">{st.session_state["script_output"]}</div>', unsafe_allow_html=True)
        st.text_area("कॉपी करने के लिए यहाँ क्लिक करें:", st.session_state['script_output'], height=400)
    else:
        st.info("👈 बाईं ओर से किसी न्यूज़ पर क्लिक करें।")

# नीचे की पट्टी
st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak Studio: जलगाँव की हर बड़ी खबर की स्क्रिप्ट अब आपके हाथ में...</marquee></div>', unsafe_allow_html=True)
