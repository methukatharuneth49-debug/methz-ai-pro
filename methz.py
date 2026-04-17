import streamlit as st
from groq import Groq
from PIL import Image

# --- 1. PAGE CONFIG & LAYOUT ---
st.set_page_config(page_title="METHZ AI Pro", page_icon="logo.png", layout="centered")

# Custom CSS for Message Alignment & Styling
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 10px;
    }
    /* Hide User Avatar if possible via CSS */
    [data-testid="stChatMessageAvatarUser"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Creator & Version Info) ---
with st.sidebar:
    st.title("Settings & Info")
    try:
        side_img = Image.open("logo.png")
        st.image(side_img, width=100)
    except:
        pass
    st.markdown("---")
    st.write(" **Creator:** Methuka")
    st.write(" **Model:** METHZ AI Pro")
    st.write(" **Version:** 2.0 (Trilingual)")
    st.markdown("---")
    st.caption("All rights reserved © 2024")

# --- 3. MAIN INTERFACE ---
try:
    img = Image.open("logo.png")
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(img, width=80)
    with col2:
        st.title("METHZ AI Pro")
except:
    st.title("METHZ AI Pro")

st.markdown("---")

# --- 4. API SETUP ---
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = "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" # Local testing වලට විතරයි

client = Groq(api_key=API_KEY)

# --- 5. SESSION STATE (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 6. DISPLAY CHAT MESSAGES ---
for message in st.session_state.messages:
    # User ට avatar එකක් නැතිව පෙන්වන්න avatar=None දාලා තියෙනවා
    avatar_img = None if message["role"] == "user" else "logo.png"
    with st.chat_message(message["role"], avatar=avatar_img):
        st.markdown(message["content"])

# --- 7. INPUT & RESPONSE ---
if user_input := st.chat_input("Ask Anything"):
    # User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=None):
        st.markdown(user_input)

    # AI Response
    with st.chat_message("assistant", avatar="logo.png"):
        placeholder = st.empty()
        
        try:
            # සිංහල අකුරු අතරට ඉංග්‍රීසි වචන (METHZ, Methuka) Mix කරන prompt එක
            system_prompt = (
                "Your name is METHZ AI. You were created by Methuka. "
                "You are a close friend of the user. Mix English, Sinhala script, and Singlish naturally. "
                "CRITICAL RULE: Even when you are typing in Sinhala script, ALWAYS write 'METHZ AI' and 'Methuka' "
                "in English letters. Do not write them in Sinhala letters. "
                "For example: 'අඩෝ මචං, මාව හැදුවේ Methuka!' "
                "If the user says 'sinhalen kiyapan', use Sinhala script but keep 'METHZ' and 'Methuka' in English. "
                "Be informal, funny, and cool. Use slang like 'Ado', 'Machan', 'Patta', 'Sira'."
            )
            
            history = [{"role": "system", "content": system_prompt}] + \
                      [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

            # අලුත්ම Model එක භාවිතා කර ඇත
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=history,
                stream=False
            )
            
            full_response = completion.choices[0].message.content
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Ayo error ekak mchan: {e}")