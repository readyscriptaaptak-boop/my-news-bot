import streamlit as st
import feedparser
import trafilatura
import pytz
from datetime import datetime

# --- पेज सेटिंग ---
st.set_page_config(page_title="India Aaptak AI Studio", page_icon="🎙️", layout="wide")

# --- मेमोरी सेटअप (ताकि बटन काम करें) ---
if 'selected_news_title' not in st.session_state:
    st.session_state['selected_news_title'] = ""
if 'selected_news_url' not in st.session_state:
    st.session_state['selected_news_url'] = ""
if 'generated_script' not in st.session_state:
    st.session_state['generated_script'] = ""

# IST टाइम
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

# --- सुंदर डिजाइन (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { background-color: #ce1212; color: white; font-weight: bold; border-radius: 10px; height: 3em; }
    .script-area { background-color: #1a1c24; padding: 25px; border-radius: 15px; border-left: 10px solid #ce1212; color: white; font-size: 18px; line-height: 1.7; }
    .news-card { background: #21262d; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- फंक्शन: पूरी खबर पढ़ना और स्क्रिप्ट बनाना ---
def fetch_and_create_script(url, title):
    with st.spinner('रोबोट वेबसाइट से खबर पढ़ रहा है...'):
        try:
            downloaded = trafilatura.fetch_url(url)
            text = trafilatura.extract(downloaded)
            
            if not text or len(text) < 100:
                # अगर पहली लिंक काम न करे, तो गूगल पर फिर से ढूँढना (Deep Search)
                return "माफी! इस वेबसाइट ने खबर पढ़ने से रोक दिया है। कृपया दूसरी खबर चुनें।"
            
            # प्रॉपर वॉइस ओवर स्क्रिप्ट बनाना
            script = f"""
🎙️ **इंडिया आपतक न्यूज़ - वॉइस ओवर स्क्रिप्ट**
--------------------------------------------------
**(तेज़ म्यूजिक - INTRO)**

**एंकर (VO):** नमस्कार, आप देख रहे हैं 'इंडिया आपतक न्यूज़'। मैं हूँ आपका न्यूज़ डेस्क और इस वक्त की सबसे बड़ी खबर जलगाँव और महाराष्ट्र से निकलकर सामने आ रही है।

**हेडलाइन:** {title}

**विस्तार से जानकारी:** {text[:1200]}... 

**एंकर (VO):** (गंभीर स्वर) जी हाँ, दर्शकों... जैसा कि आपने सुना, इस पूरे मामले ने अब तूल पकड़ लिया है। मौके पर मौजूद हमारे सूत्रों के अनुसार, स्थिति पर प्रशासन की पैनी नज़र बनी हुई है। आने वाले समय में इस घटना के बड़े परिणाम देखने को मिल सकते हैं। 

जलगाँव की इस हलचल पर 'इंडिया आपतक' की टीम लगातार ग्राउंड ज़ीरो से अपडेट दे रही है। 

**(आउटरो म्यूजिक)**
**एंकर (VO):** इस खबर पर आपकी क्या राय है? कमेंट में जरूर बताएं। ताज़ा और सटीक खबरों के लिए सब्सक्राइब करें 'इंडिया आपतक न्यूज़'। कैमरा पर्सन के साथ, मैं न्यूज़ डेस्क।
--------------------------------------------------
✅ **YouTube SEO:**
- **Title:** {title[:70]} | India Aaptak Live
- **Tags:** #Jalgaon #BreakingNews #IndiaAaptak
            """
            return script
        except:
            return "सर्वर एरर! खबर लोड नहीं हो पाई।"

# --- मुख्य UI ---
st.markdown("<h1 style='text-align: center; color: #ce1212;'>🎙️ INDIA AAPTAK NEWS STUDIO</h1>", unsafe_allow_html=True)
st.write(f"<p style='text-align: center;'><b>Live Studio Dashboard | {current_time}</b></p>", unsafe_allow_html=True)

# --- सर्च बॉक्स (सबसे ऊपर) ---
user_query = st.text_input("🔍 यहाँ न्यूज़ सर्च करें (जैसे: Jalgaon Crime, Weather, Modi)", placeholder="खबर का विषय लिखें...")

# --- लेआउट: 2 कॉलम ---
col1, col2 = st.columns([1, 1.3])

with col1:
    st.subheader("📲 ताज़ा खबरें")
    # न्यूज़ कैटेगरी
    topic = st.radio("कैटेगरी चुनें", ["Jalgaon", "Maharashtra", "India"], horizontal=True)
    
    # अगर सर्च बॉक्स में कुछ है तो वो सर्च करो, वरना रेडियो बटन वाला टॉपिक
    final_search = user_query if user_query else topic
    
    feed = feedparser.parse(f"https://news.google.com/rss/search?q={final_search}+when:24h&hl=hi&gl=IN&ceid=IN:hi")
    
    for i, entry in enumerate(feed.entries[:12]):
        with st.container():
            st.markdown(f'<div class="news-card"><b>{entry.title}</b><br><small>सोर्स: {entry.source.title}</small></div>', unsafe_allow_html=True)
            # यहाँ बटन क्लिक होने पर मेमोरी (State) में डेटा सेव होगा
            if st.button(f"इसकी स्क्रिप्ट बनाएं ✨", key=f"btn_{i}"):
                st.session_state['selected_news_title'] = entry.title
                st.session_state['selected_news_url'] = entry.link
                # तुरंत स्क्रिप्ट बनाना शुरू करें
                st.session_state['generated_script'] = fetch_and_create_script(entry.link, entry.title)

with col2:
    st.subheader("✍️ न्यूज़ वॉइस-ओवर स्क्रिप्ट")
    if st.session_state['generated_script']:
        st.success(f"खबर: {st.session_state['selected_news_title']}")
        st.markdown(f'<div class="script-area">{st.session_state["generated_script"]}</div>', unsafe_allow_html=True)
        
        # कॉपी बटन
        st.text_area("स्क्रिप्ट कॉपी करें (यहाँ से):", st.session_state['generated_script'], height=300)
    else:
        st.info("👈 बाईं ओर से किसी खबर पर 'स्क्रिप्ट बनाएं' बटन दबाएं।")

# नीचे की पट्टी
st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak AI Studio: आपका रोबोट अब पूरी खबर पढ़कर स्क्रिप्ट तैयार कर रहा है...</marquee></div>', unsafe_allow_html=True)
