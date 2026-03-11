import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import trafilatura
import pytz
from datetime import datetime
from urllib.parse import quote

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
    .main-header { background: linear-gradient(90deg, #ce1212, #8b0000); padding: 15px; border-radius: 12px; color: white; text-align: center; margin-bottom: 20px;}
    .script-box { background: #161b22; padding: 25px; border-radius: 12px; border-left: 8px solid #ffbd45; color: #f0f6fc; font-size: 19px; line-height: 1.8; }
    .news-card { background: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 12px; transition: 0.3s; }
    .news-card:hover { border-color: #ce1212; background: #252a33; }
    .source-tag { background: #ce1212; color: white; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- न्यूज़ रीडर फंक्शन ---
def smart_scrape(target_title):
    encoded_title = quote(target_title)
    search_url = f"https://news.google.com/rss/search?q={encoded_title}&hl=hi&gl=IN&ceid=IN:hi"
    search_feed = feedparser.parse(search_url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
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
        except: continue
    return None, None

def generate_script(title, body, source):
    return f"""
🎙️ **INDIA AAPTAK NEWS: वॉइस-ओवर स्क्रिप्ट**
--------------------------------------------------
**(तेज़ न्यूज़ म्यूजिक - INTRO)**

**एंकर (VO):** नमस्कार, आप देख रहे हैं 'इंडिया आपतक न्यूज़'। इस वक्त की बड़ी और ताज़ा खबर के साथ मैं हूँ आपका न्यूज़ डेस्क।

**हेडलाइन:** {title}

**खबर का विस्तार:** {body[:1500]}

**(गंभीर स्वर में)**
**एंकर (VO):** जी हाँ, दर्शकों... जैसा कि जानकारी मिल रही है, **{source}** के हवाले से यह खबर इस वक्त सुर्खियों में बनी हुई है। प्रशासन पूरी तरह से अलर्ट पर है।

ताज़ा अपडेट्स के लिए बने रहें 'इंडिया आपतक न्यूज़' के साथ। 

**(आउटरो म्यूजिक)**
**एंकर (VO):** कैमरा पर्सन के साथ, मैं न्यूज़ डेस्क। जय हिन्द!
--------------------------------------------------
✅ #Jalgaon #MaharashtraNews #IndiaAaptak
    """

st.markdown('<div class="main-header"><h1>INDIA AAPTAK AI STUDIO 🎙️</h1></div>', unsafe_allow_html=True)
st.write(f"<p style='text-align:center;'><b>खबरों का बाज़ार | ⚡ {current_time}</b></p>", unsafe_allow_html=True)

# --- सर्च बार ---
s_query = st.text_input("🔍 ब्रेकिंग न्यूज़ सर्च करें", placeholder="यहाँ विषय लिखें...")

c1, c2 = st.columns([1.1, 1.2])

with c1:
    st.subheader("🔥 ताज़ा खबरें (Top 20)")
    base_topic = st.radio("कैटेगरी", ["Jalgaon", "Maharashtra", "India"], horizontal=True)
    
    # समय सीमा: पिछले 12 घंटे और ताज़ा खबरों के लिए कीवर्ड्स
    search_addon = "Breaking+News"
    final_q = s_query if s_query else f"{base_topic}+{search_addon}"
    
    main_feed_url = f"https://news.google.com/rss/search?q={quote(final_q)}+when:12h&hl=hi&gl=IN&ceid=IN:hi"
    feed = feedparser.parse(main_feed_url)
    
    # --- डुप्लीकेट फिल्टर लॉजिक ---
    unique_titles = []
    unique_entries = []
    
    for entry in feed.entries:
        # खबर के शुरूआती 25 अक्षर चेक करना ताकि डुप्लीकेट न आए
        short_title = entry.title[:25]
        if short_title not in unique_titles:
            unique_titles.append(short_title)
            unique_entries.append(entry)
        if len(unique_entries) >= 20: # 20 न्यूज़ की लिमिट
            break

    for i, e in enumerate(unique_entries):
        with st.container():
            st.markdown(f'''
                <div class="news-card">
                    <span class="source-tag">{e.source.title}</span>
                    <div style="margin-top:8px;"><b>{e.title}</b></div>
                </div>
            ''', unsafe_allow_html=True)
            
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                if st.button(f"स्क्रिप्ट बनाएं ✨", key=f"btn_{i}"):
                    with st.spinner('रोबोट ताज़ा जानकारी पढ़ रहा है...'):
                        full_text, found_source = smart_scrape(e.title)
                        if full_text:
                            st.session_state['final_script'] = generate_script(e.title, full_text, found_source)
                        else:
                            st.error("माफी! डिटेल नहीं मिली।")
            with b_col2:
                st.link_button("सोर्स देखें 🔗", e.link)

with c2:
    st.subheader("📝 प्रोफेशनल स्क्रिप्ट")
    if st.session_state['final_script']:
        st.markdown(f'<div class="script-box">{st.session_state["final_script"]}</div>', unsafe_allow_html=True)
        st.text_area("कॉपी करें:", st.session_state['final_script'], height=550)
    else:
        st.info("👈 बाईं ओर से ताज़ा न्यूज़ चुनें।")

st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak AI Studio: जलगाँव और देश-विदेश की 20-20 ताज़ा खबरें यहाँ उपलब्ध हैं...</marquee></div>', unsafe_allow_html=True)
