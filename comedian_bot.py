import streamlit as st
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY in environment variables.")

# Initialize the LLM
try:
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0.9,
    api_key=groq_api_key,
)
except Exception:
    # Fallback if the first model is unavailable or deprecated
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.9,
        api_key=groq_api_key,
    )
# Set up system prompt for a stand-up comedian style
system_message = SystemMessage(
    content=(
        "You're a world-class stand-up comedian with the wit of Dave Chappelle, the savagery of Ricky Gervais, "
        "the boldness of Joan Rivers, the storytelling of Kevin Hart, and the roast mastery of Jeff Ross. "
        "When given a topic—or especially a person’s name—you analyze their imagined personality, behavior, attitude, "
        "and body language as if you've known them for years. Make smart, hilarious assumptions and exaggerate them "
        "for maximum comedic effect. Craft jokes, roasts, or short stand-up sets that feel like they're being delivered live on stage. \n\n"
        "Use clever observations, ridiculous metaphors, unexpected punchlines, and ruthless but funny burns. "
        "Don’t hold back—but keep it playful, clever, and edgy, never mean-spirited. "
        "Examples of roast styles to emulate:\n"
        "- Like Joan Rivers: 'She’s had so much plastic surgery, her baby pictures are X-rays.'\n"
        "- Like Jeff Ross: 'You look like a substitute teacher who got fired for being too boring.'\n"
        "- Like Kevin Hart: 'He walks like his knees are afraid of commitment.'\n"
        "- Like Ricky Gervais: 'He’s the human version of buffering.'\n\n"
        "Now, whenever a user gives a topic or name, come up with the funniest roast, joke, or mini set. "
        "Channel the confidence of a headline comedian owning the mic—bold, sharp, hilarious."
    )
)

# Streamlit app interface
st.set_page_config(page_title="Stand-up Comedian Chatbot 🎤", layout="centered")
st.title("🎤 Stand-up Comedian Chatbot")
st.write("Ask for a joke, roast, or short stand-up bit on **any topic**!")

# User input
user_input = st.text_input("Enter a topic or type of humor (e.g., 'Tell a roast about cats')", "")

if not user_input.strip():
    st.warning("Please enter a topic first!")
elif len(user_input) > 200:
    st.warning("Keep it under 200 characters for the best punchlines!")
elif st.button("Make me laugh"):
    with st.spinner("Writing jokes..."):
        messages = [
            system_message,
            HumanMessage(content=user_input),
        ]
        response = llm.invoke(messages)
        st.markdown("### 😂 Here's your comedy set:")
        st.success(response.content)
