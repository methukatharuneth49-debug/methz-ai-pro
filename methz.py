import streamlit as st
from groq import Groq
from PIL import Image

# --- 1. LOGO & PAGE CONFIG ---
try:
    logo_img = Image.open("logo.png")
except:
    logo_img = None

st.set_page_config(page_title="METHZ AI Pro", page_icon=logo_img if logo_img else "🤖", layout="wide")

# --- 2. THE FINAL CSS FIX (True Alignment) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Container for all bubbles */
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        width: 100%;
        gap: 10px;
    }

    /* Common bubble style */
    .bubble {
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 75%;
        font-family: 'Segoe UI', sans-serif;
        margin-bottom: 5px;
        display: inline-block;
    }

    /* USER BUBBLE: Force to RIGHT */
    .user-container {
        display: flex;
        justify-content: flex-end; /* මේකෙන් තමයි දකුණට කරන්නේ */
        width: 100%;
    }
    .user-bubble {
        background-color: #1e293b;
        color: white;
        border-bottom-right-radius: 2px;
    }

    /* AI BUBBLE: Force to LEFT */
    .ai-container {
        display: flex;
        justify-content: flex-start;
        width: 100%;
    }
    .ai-bubble {
        background-color: #0f172a;
        color: #e2e8f0;
        border: 1px solid #334155;
        border-bottom-left-radius: 2px;
    }

    /* Hide Default Streamlit Elements */
    [data-testid="stChatAvatarContainer"] { display: none !important; }
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; }
    
    .header-text { font-size: 32px; font-weight: bold; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("METHZ AI")
    st.markdown("---")
    if st.button("Clear Chat 🗑️"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.info("Created by **Methuka**")
    st.caption("Version 3.1 Pro")

# --- 4. HEADER ---
col_logo, col_title = st.columns([0.07, 0.93])
with col_logo:
    if logo_img: st.image(logo_img, width=55)
    else: st.write("🤖")
with col_title:
    st.markdown('<div class="header-text">METHZ AI Pro</div>', unsafe_allow_html=True)

# --- 6. API SETUP ---
# කලින් තිබ්බ පරණ පේළිය අයින් කරලා මේක දාන්න:
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    # මේක ලැප් එකේදී (Local) රන් කරද්දී ඕන වෙනවා
    API_KEY = "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"

client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 6. DISPLAY CHAT ---
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-container"><div class="bubble user-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-container"><div class="bubble ai-bubble">{msg["content"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# මේක තමයි English + Sinhala + Singlish ඔක්කොම තියෙන සුපිරි prompt එක
system_prompt = (
                "You are a close friend of the user. You are fluent in English, "
                "Sinhala, and Singlish. Mix these languages naturally like a typical "
                "Sri Lankan youth. Use words like 'Ado', 'Machan', 'අඩෝ', 'මචං', 'Patta', 'Siraawata'. "
                "If the user speaks in English, you can reply in English or mix it with Singlish. "
                "Be informal, funny, and cool. Keep your answers short and friendly."
            )
history = [{"role": "system", "content": system_prompt}] + \
    [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]