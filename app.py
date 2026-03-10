import streamlit as st
import feedparser
import pytz
from datetime import datetime

# IST समय सेटअप
IST = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(IST).strftime('%I:%M %p')

st.set_page_config(page_title="India Aaptak AI Studio", page_icon="🎙️", layout="wide")

# प्रोफेशनल स्टाइलिंग
st.markdown("""
    <style>
    .anchor-script { background-color: #fdf2f2; padding: 25px; border-radius: 15px; border: 2px solid #ce1212; color: #1a1a1a; font-size: 18px; line-height: 1.6; }
    .ticker-box { background: #1e1e1e; color: #ffbd45; padding: 10px; border-radius: 5px; margin-bottom: 5px; font-weight: bold; }
    .whatsapp-box { background: #e3ffe6; padding: 15px; border-radius: 10px; border-left: 5px solid #25d366; color: black; }
    </style>
""", unsafe_allow_html=True)

# --- TTD & Script Generator Engine ---
def generate_pro_content(headline):
    # 5 शब्द (Keywords)
    keywords = ", ".join(headline.split()[:5])
    
    # 10 टिकर (News Tickers)
    tickers = [f"बड़ी खबर: {headline}", "इंडिया आपतक न्यूज़ अपडेट", "जलगाँव की ताज़ा हलचल", "प्रशासन अलर्ट पर", "देखें पूरी रिपोर्ट", "ब्रेकिंग न्यूज़", "पब्लिक की राय", "ग्राउंड जीरो से रिपोर्ट", "Exclusive", "बने रहें हमारे साथ"]
    
    # एंकर स्क्रिप्ट (Direct Voice-over)
    anchor_script = f"""
🎤 **ANCHOR VOICE-OVER START:**
(तेज़ म्यूज़िक...)
नमस्कार! मैं हूँ आपका न्यूज़ एंकर और आप देख रहे हैं **'इंडिया आपतक न्यूज़'**। 

इस वक्त की एक बेहद बड़ी और सनसनीखेज खबर **{headline}** से जुड़ी हुई सामने आ रही है। 

जी हाँ, दर्शकों... ये खबर इस वक्त तेज़ी से वायरल हो रही है और इलाके में चर्चा का विषय बनी हुई है। हमारे पास जो शुरुआती जानकारी है, उसके मुताबिक इस पूरे मामले ने अब एक नया मोड़ ले लिया है। मौके पर हमारी टीम पहुँच चुकी है और हम आपको पल-पल की जानकारी दे रहे हैं। 

(पाउज़...)

क्या है इस पूरी खबर की सच्चाई? क्यों मचा है इतना बवाल? देखिए हमारी ये विशेष रिपोर्ट!
    """
    
    return keywords, tickers, anchor_script

st.title("🎙️ India Aaptak: AI न्यूज़ स्टूडियो")
st.write(f"ताज़ा अपडेट: {current_time} | लोकेशन: जलगाँव")

# न्यूज़ फेचिंग
@st.cache_data(ttl=300)
def get_news(q):
    return feedparser.parse(f"https://news.google.com/rss/search?q={q}+when:12h&hl=hi&gl=IN&ceid=IN:hi").entries[:15]

# --- UI Layout ---
left, right = st.columns([1, 1.2])

with left:
    st.header("📲 न्यूज़ चुनें")
    cat = st.radio("कैटेगरी", ["Jalgaon", "Maharashtra", "India"], horizontal=True)
    items = get_news(cat)
    for i, n in enumerate(items):
        if st.button(f"📄 {n.title[:60]}...", key=f"n_{i}"):
            st.session_state['active_news'] = n.title
            st.session_state['active_link'] = n.link

with right:
    st.header("✍️ रेडी-मेड स्क्रिप्ट")
    if 'active_news' in st.session_state:
        title = st.session_state['active_news']
        k, t, script = generate_pro_content(title)
        
        # एंकर स्क्रिप्ट सेक्शन
        st.subheader("1. 🎙️ वॉइस-ओवर स्क्रिप्ट")
        st.markdown(f'<div class="anchor-script">{script}</div>', unsafe_allow_html=True)
        
        # TTD सेक्शन
        st.subheader("2. 📺 10 टिकर (Scroll)")
        for tic in t:
            st.markdown(f'<div class="ticker-box">{tic}</div>', unsafe_allow_html=True)
            
        # SEO & WhatsApp
        st.subheader("3. 📱 सोशल मीडिया शेयर")
        wa_text = f"🚨 *ब्रेकिंग न्यूज़: इंडिया आपतक* 🚨\n\n*{title}*\n\nपूरे वीडियो के लिए यहाँ क्लिक करें: \n{st.session_state['active_link']}\n\n#Jalgaon #IndiaAaptak #Breaking"
        st.markdown(f'<div class="whatsapp-box">{wa_text}</div>', unsafe_allow_html=True)
        st.button("कॉपी करें (Copy)", on_click=lambda: st.write("Copied!"))
        
    else:
        st.info("बाएं हाथ की लिस्ट में से किसी खबर पर क्लिक करें, उसकी स्क्रिप्ट यहाँ आ जाएगी।")

# नीचे चलने वाली पट्टी
st.markdown('<div style="position:fixed; bottom:0; left:0; width:100%; background:#ce1212; color:white; padding:5px;"><marquee>India Aaptak AI News Studio: खबरें चुनें और रिकॉर्डिंग शुरू करें...</marquee></div>', unsafe_allow_html=True)
