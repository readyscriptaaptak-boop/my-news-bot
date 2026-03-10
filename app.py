import streamlit as st
import feedparser
import pytz
import trafilatura
from datetime import datetime

# IST समय सेटअप
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

st.set_page_config(page_title="India Aaptak - Ready Script", page_icon="🎙️", layout="wide")

# प्रोफेशनल स्टाइलिंग (Newsroom Look)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .script-box { 
        background-color: #1a1c24; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 8px solid #ce1212; 
        color: #ffffff; 
        font-size: 19px; 
        line-height: 1.8;
        font-family: 'Arial';
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .news-item { background: #21262d; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #30363d; }
    .status-tag { color: #ffbd45; font-weight: bold; font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# --- असली खबर खोजने वाला इंजन (Multi-Link Search) ---
def get_best_content(title_to_search):
    # यह उसी खबर को अलग-अलग सोर्सेज से सर्च करता है
    search_url = f"https://news.google.com/rss/search?q={title_to_search}&hl=hi&gl=IN&ceid=IN:hi"
    feed = feedparser.parse(search_url)
    
    # पहली 3 वेबसाइट्स को चेक करना (ताकि जानकारी पक्की मिले)
    for entry in feed.entries[:3]:
        try:
            downloaded = trafilatura.fetch_url(entry.link)
            content = trafilatura.extract(downloaded)
            if content and len(content) > 300: # अगर खबर 300 शब्दों से बड़ी है
                return content, entry.source.title
        except:
            continue
    return None, None

# --- प्रो-स्क्रिप्ट राइटर (Voice-over Logic) ---
def create_pro_script(title, full_text, source_name):
    # स्क्रिप्ट का प्रॉपर न्यूज़ फॉर्मेट
    script = f"""
🎙️ **INDIA AAPTAK NEWS - प्रॉपर वॉइस ओवर स्क्रिप्ट**
--------------------------------------------------
**(तेज़ न्यूज़ म्यूजिक - INTRO)**

**एंकर (VO):** नमस्कार, आप देख रहे हैं 'इंडिया आपतक न्यूज़'। जलगाँव और महाराष्ट्र की इस बड़ी खबर के साथ मैं हूँ आपका न्यूज़ डेस्क।

**मुख्य समाचार:** {title}

**विस्तार से:** {full_text[:800]}...

**एंकर (VO):** (गंभीर स्वर में) जी हाँ, जैसा कि जानकारी मिल रही है, इस पूरे मामले ने अब प्रशासन और जनता का ध्यान अपनी ओर खींच लिया है। सूत्रों के मुताबिक, **{source_name}** द्वारा दी गई जानकारी के अनुसार, आने वाले दिनों में इस पर और भी बड़े फैसले लिए जा सकते हैं। 

इस खबर की तकनीकी बारीकियों को देखें तो साफ पता चलता है कि यह सीधे तौर पर आम जनता से जुड़ी हुई है। मौके पर हमारी टीम बनी हुई है और पल-पल की अपडेट्स आप तक पहुँचाई जा रही है।

**(आउटरो म्यूजिक)**
**एंकर (VO):** इस पूरी खबर पर हमारी नज़र बनी रहेगी। ताज़ा अपडेट्स और ग्राउंड रिपोर्ट के लिए देखते रहिए 'इंडिया आपतक न्यूज़'। कैमरा पर्सन के साथ, मैं न्यूज़ डेस्क।
--------------------------------------------------
✅ **SEO के लिए:**
- **YouTube Title:** {title[:70]} | India Aaptak Live
- **Hashtags:** #Jalgaon #MaharashtraNews #IndiaAaptak
    """
    return script

st.title("🎙️ India Aaptak: डिजिटल न्यूज़ स्टूडियो")
st.write(f"ताज़ा अपडेट (IST): {current_time}")

# न्यूज़ लोड करना
@st.cache_data(ttl=600)
def fetch_news_list(q):
    return feedparser.parse(f"https://news.google.com/rss/search?q={q}+when:12h&hl=hi&gl=IN&ceid=IN:hi").entries[:15]

c1, c2 = st.columns([1, 1.5])

with c1:
    st.header("📲 खबर चुनें")
    cat = st.radio("कैटेगरी", ["Jalgaon", "Maharashtra", "India"], horizontal=True)
    items = fetch_news_list(cat)
    
    for i, n in enumerate(items):
        with st.container():
            st.markdown(f'<div class="news-item"><span class="status-tag">Live</span><br><b>{n.title}</b></div>', unsafe_allow_html=True)
            if st.button(f"रेडी-मेड स्क्रिप्ट तैयार करें ✨", key=f"btn_{i}"):
                st.session_state['target_title'] = n.title

with c2:
    st.header("📝 प्रोफेशनल स्क्रिप्ट")
    if 'target_title' in st.session_state:
        with st.spinner('रोबोट इंटरनेट खंगाल रहा है और पूरी खबर पढ़ रहा है...'):
            # मल्टी-सोर्स से पूरी खबर निकालना
            full_raw_text, real_source = get_best_content(st.session_state['target_title'])
            
            if full_raw_text:
                # स्क्रिप्ट बनाना
                final_script = create_pro_script(st.session_state['target_title'], full_raw_text, real_source)
                st.markdown(f'<div class="script-box">{final_script}</div>', unsafe_allow_html=True)
                st.download_button("स्क्रिप्ट फाइल डाउनलोड करें", final_script, file_name="news_script.txt")
            else:
                st.error("माफ़ी! इस खबर की विस्तृत जानकारी किसी भी ओपन पोर्टल पर नहीं मिल पाई। कृपया दूसरी खबर चुनें।")
    else:
        st.info("बाईं ओर से कोई भी 'ताज़ा खबर' चुनें, रोबोट उसकी पूरी डिटेल निकालकर आपको स्क्रिप्ट दे देगा।")

st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak AI: आपका रोबोट अब मल्टी-सोर्स से खबरें पढ़ रहा है... एकदम सटीक और ताज़ा जानकारी...</marquee></div>', unsafe_allow_html=True)
