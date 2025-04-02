import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Custom CSS for WhatsApp-style chat UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

    body {
        font-family: 'Roboto', sans-serif;
    }
    .chat-container {
        max-width: 600px;
        margin: auto;
    }
    .user-msg {
        background-color: #DCF8C6; /* WhatsApp green */
        text-align: right;
        padding: 12px;
        border-radius: 12px;
        margin: 5px 0;
        float: right;
        clear: both;
        max-width: 70%;
        font-family: 'Roboto', sans-serif;
    }
    .bot-msg {
        background-color: #E5E5EA; /* WhatsApp gray */
        text-align: left;
        padding: 12px;
        border-radius: 12px;
        margin: 5px 0;
        float: left;
        clear: both;
        max-width: 70%;
        font-family: 'Roboto', sans-serif;
    }
    .sentiment-box {
        display: block;
        padding: 6px;
        border-radius: 6px;
        font-weight: bold;
        margin: 10px auto;
        max-width: 200px;
        text-align: center;
    }
    .positive { background-color: #D4EDDA; color: #155724; } /* Green */
    .neutral { background-color: #FFF3CD; color: #856404; } /* Yellow */
    .negative { background-color: #F8D7DA; color: #721C24; } /* Red */
    .clear { clear: both; }
    </style>
""", unsafe_allow_html=True)

st.title("💬 WhatsApp-Style Customer Support")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a friendly customer support assistant, responding like a helpful agent."}
    ]

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":  # Don't display system messages
        css_class = "user-msg" if msg["role"] == "user" else "bot-msg"
        st.markdown(f'<div class="{css_class}">{msg["content"]}</div><div class="clear"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

user_input = st.chat_input("Type your message here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message (right-aligned)
    st.markdown(f'<div class="user-msg">{user_input}</div><div class="clear"></div>', unsafe_allow_html=True)

    # Sentiment Analysis
    sentiment_response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Analyze the sentiment of the following text and classify it as Positive, Negative, or Neutral. Respond with only one word: Positive, Negative, or Neutral."},
            {"role": "user", "content": user_input},
        ]
    )
    sentiment_text = sentiment_response.choices[0].message.content.strip()

    # Sentiment Mapping
    sentiment_emojis = {
        "Positive": "🟢😊",
        "Neutral": "🟡😐",
        "Negative": "🔴😠"
    }
    sentiment_classes = {
        "Positive": "positive",
        "Neutral": "neutral",
        "Negative": "negative"
    }
    sentiment_emoji = sentiment_emojis.get(sentiment_text, "⚪🤖")
    sentiment_class = sentiment_classes.get(sentiment_text, "neutral")

    # Get AI Response
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=st.session_state.messages
    )

    bot_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Display sentiment and assistant response (left-aligned)
    st.markdown(f'<div class="sentiment-box {sentiment_class}">{sentiment_emoji} {sentiment_text}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-msg">{bot_reply}</div><div class="clear"></div>', unsafe_allow_html=True)
