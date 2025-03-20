import streamlit as st
import time
from backend import generate_flashcards

# 1. Page Configuration
st.set_page_config(page_title="AI Flashcard Generator", layout="centered")

st.title("📚 AI Flashcard Generator")
st.write("Generate AI-powered flashcards on any topic!")

# 2. Custom Style
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: white !important;
        color: black !important;
    }
    .stButton > button {
        background-color: #695959 !important;
        color: white !important;
        border: 1px solid #695959 !important;
        border-radius: 5px !important;
        padding: 0.4rem 1rem;
        cursor: pointer;
    }
    .stButton > button:hover {
        background-color: #3f3636 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Define the Cute Loading GIF (Tenor link)
LOADING_BAR_URL = "https://media.tenor.com/Kwq2I-vIuOQAAAAi/downsign-loading.gif"

# 4. Create/Manage Session State
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# 5. Input for Topic
topic = st.text_input("Enter a topic for flashcards:")

# 6. Button to Generate Flashcards
if st.button("Generate Flashcards"):
    if topic.strip():
        # Create a placeholder for the loading animation
        loading_placeholder = st.empty()

        # Fill the placeholder with a loading message, the GIF, and a progress bar
        with loading_placeholder.container():
            st.write("### Magically flying across the world to find your flashcards, please wait...")
            st.image(LOADING_BAR_URL, width=300)


        # Generate flashcards (this might take some time depending on your LLM)
        flashcards = generate_flashcards(topic)

        # Clear the placeholder once generation is done
        loading_placeholder.empty()

        if flashcards and isinstance(flashcards, list):
            st.session_state.flashcards = flashcards
            st.session_state.current_index = 0  # reset to first card
            st.success("Flashcards generated successfully!")
        else:
            st.error("No flashcards were generated. Please try a different topic.")
    else:
        st.warning("Please enter a topic before generating flashcards.")

# 7. Display Flashcards (if any)
if st.session_state.flashcards:
    st.header("Flashcards")
    current_flashcard = st.session_state.flashcards[st.session_state.current_index]
    
    # Validate the flashcard structure
    if not (isinstance(current_flashcard, dict) and "question" in current_flashcard and "answer" in current_flashcard):
        st.error("Flashcard format is incorrect. Please regenerate flashcards.")
    else:
        question = current_flashcard["question"]
        answer = current_flashcard["answer"]
        
        # Flip-card HTML
        with st.container():
            html_code = f"""
            <html>
              <head>
                <style>
                  .flip-card {{
                    background-color: transparent;
                    width: 400px;
                    height: 250px;
                    perspective: 1000px;
                    margin: auto;
                  }}
                  .flip-card-inner {{
                    position: relative;
                    width: 100%;
                    height: 100%;
                    text-align: center;
                    transition: transform 0.6s;
                    transform-style: preserve-3d;
                  }}
                  .flip-card-inner.flipped {{
                    transform: rotateY(180deg);
                  }}
                  .flip-card-front, .flip-card-back {{
                    position: absolute;
                    width: 100%;
                    height: 100%;
                    backface-visibility: hidden;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 24px;
                    padding: 20px;
                  }}
                  .flip-card-front {{
                    background-color: #dbbdbd;
                    color: #3f3636;
                  }}
                  .flip-card-back {{
                    background-color: #a8a8d7;
                    color: #3f3636;
                    transform: rotateY(180deg);
                  }}
                </style>
                <script>
                  function flipCard() {{
                      var inner = document.getElementById("card-inner");
                      inner.classList.toggle("flipped");
                  }}
                </script>
              </head>
              <body>
                <div class="flip-card" onclick="flipCard()">
                  <div class="flip-card-inner" id="card-inner">
                    <div class="flip-card-front">
                      {question}
                    </div>
                    <div class="flip-card-back">
                      {answer}
                    </div>
                  </div>
                </div>
              </body>
            </html>
            """
            st.components.v1.html(html_code, height=300, scrolling=False)

        # Navigation buttons
        col_left, col_spacer, col_right = st.columns([3, 10, 3])
        with col_left:
            if st.button("⬅️ Previous", key="prev"):
                if st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
        with col_right:
            if st.button("Next ➡️", key="next"):
                if st.session_state.current_index < len(st.session_state.flashcards) - 1:
                    st.session_state.current_index += 1
