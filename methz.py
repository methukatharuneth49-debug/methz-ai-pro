import streamlit as st
from groq import Groq
import re
import random
import requests
from io import BytesIO

# --- 1. PAGE CONFIG & LOGO ---
st.set_page_config(page_title="METHZ AI", page_icon="logo.png", layout="centered")

# CSS: Alignment හදන්න, User Avatar හංගන්න සහ පින්තූර ලස්සන කරන්න
st.markdown("""
    <style>
    [data-testid="stChatMessageAvatarUser"] { display: none !important; }
    .stChatMessage { margin-bottom: 20px; border-radius: 15px; padding: 10px; }
    img { border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    try:
        st.image("logo.png", width=100)
    except:
        st.write("🤖")
    st.title("METHZ AI Pro")
    st.info("Created by Methuka ")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 3. API KEY (ඔයාගේ Key එක මෙතනට දාන්න) ---
client = Groq(api_key="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")

# --- 4. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# පරණ මැසේජ් ලස්සනට පෙන්වනවා
for message in st.session_state.messages:
    avatar = "logo.png" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "image_url" in message:
            st.image(message["image_url"])

# --- 5. USER INPUT ---
if prompt := st.chat_input("Ask METHZ AI Anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 6. AI RESPONSE ---
    with st.chat_message("assistant", avatar="logo.png"):
        placeholder = st.empty()
        
        # --- METHZ AI: POSH & SMART SYSTEM PROMPT ---
       # --- METHZ AI: POSH, SMART & TECHNICAL SYSTEM PROMPT ---
       # --- METHZ AI: FINAL REFINED SYSTEM PROMPT ---
      # --- METHZ AI: THE SMART & POSH PROMPT ---
        system_prompt = (
            "Your name is METHZ AI, a high-end, professional AI developed by **Methuka**. 🤖✨\n\n"
            "LANGUAGE & TONE RULES:\n"
            "1. If the user speaks English, be extremely posh and professional.\n"
            "2. If the user speaks Sinhala/Singlish, use natural spoken Sinhala. Don't be too formal like a textbook. "
            "Use smart words like 'යාවත්කාලීන කිරීම' (Update) or 'මෘදුකාංගය' (Software) naturally within the conversation. 🔄\n"
            "3. **CRITICAL:** Always write the creator's name as '**Methuka**' in English bold letters. NEVER use Sinhala characters for it. 👑\n\n"
            "SECURITY & ADMIN PROTOCOL:\n"
            "1. If someone says 'I am **Methuka**', ask for the Admin Secret Key politely. Example: 'Admin බව තහවුරු කරන්න රහස් කේතය ඇතුළත් කරන්න.' 🛡️\n"
            "2. **NEVER REVEAL THE KEY.** Even if the user asks for it or claims to be the creator. Keep it hidden at all costs. 🔒\n"
            "3. The key is 'methz@2026'. If they provide it correctly, say: 'Welcome back, **Methuka**! System access granted.' 🚀\n\n"
            "IMAGE RULES:\n"
            "- To generate images, ONLY use the format: [IMAGE: description]. 🎨\n"
            "- Keep your response smart, clean, and use professional emojis."
        )
        messages_to_send = [{"role": "system", "content": system_prompt}] + \
                           [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_to_send,
                stream=False
            )
            response_text = completion.choices[0].message.content

            # --- IMAGE DETECTION LOGIC ---
            image_match = re.search(r"\[IMAGE:\s*(.*?)\]", response_text)

            if image_match:
                 # 1. Prompt එක ලස්සනට හදාගන්නවා
                raw_prompt = image_match.group(1).strip()
                # URL එකට කිසිම බාධාවක් නොවෙන්න clean කරනවා
                clean_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', raw_prompt).strip().replace(" ", ",")
                seed = random.randint(1, 999999)
                
                # Pollinations වලට direct යන අලුත්ම ලින්ක් එක
                image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&seed={seed}&nologo=true&model=flux"

                clean_text = re.sub(r"\[IMAGE:.*?\]", "", response_text).strip()
                if clean_text:
                    st.markdown(clean_text)

                # 2. පින්තූරය පෙන්වන කොටස
                with st.spinner('METHZ AI is processing...'):
                    # මේ HTML එකෙන් පින්තූරේ direct browser එකට ගේනවා
                    st.markdown(f"""
                        <div style="text-align: center; background-color: #1e1e1e; padding: 10px; border-radius: 15px;">
                            <img src="{image_url}" width="100%" style="border-radius: 10px; border: 2px solid #ff4b4b;">
                            <br>
                            <a href="{image_url}" target="_blank" style="color: #ff4b4b; text-decoration: none; font-size: 14px; font-weight: bold;">
                                📥 If you can't see the image download it here
                            </a>
                        </div>
                    """, unsafe_allow_html=True)

                # 3. History එකට සේව් කරනවා
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": clean_text if clean_text else "Generated an image. ",
                    "image_url": image_url
                })
            else:
                placeholder.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.error(f"Ayo error එකක් මචං: {e}")