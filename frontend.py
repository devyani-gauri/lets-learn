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

# 3. Loading GIF
LOADING_BAR_URL = "https://media.tenor.com/Kwq2I-vIuOQAAAAi/downsign-loading.gif"

# 4. Session State Initialization
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# 5. Helper Functions for Next/Previous
def go_to_next_card():
    """Increment the current index if not at the end of the deck."""
    if st.session_state.current_index < len(st.session_state.flashcards) - 1:
        st.session_state.current_index += 1

def go_to_previous_card():
    """Decrement the current index if not at the beginning of the deck."""
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

# 6. Input for Topic
topic = st.text_input("Enter a topic for flashcards:")

# 7. Generate Flashcards Button
if st.button("Generate Flashcards"):
    if topic.strip():
        # Create a placeholder for the loading animation
        loading_placeholder = st.empty()

        # Fill the placeholder with a loading message & GIF
        with loading_placeholder.container():
            st.write("### Magically flying across the world to find your flashcards, please wait...")
            st.image(LOADING_BAR_URL, width=300)

        # Generate flashcards (this might take some time depending on your LLM)
        flashcards = generate_flashcards(topic)

        # Clear the placeholder once generation is done
        loading_placeholder.empty()

        if flashcards and isinstance(flashcards, list):
            st.session_state.flashcards = flashcards
            st.session_state.current_index = 0
            st.success("Flashcards generated successfully!")
        else:
            st.error("No flashcards were generated. Please try a different topic.")
    else:
        st.warning("Please enter a topic before generating flashcards.")

# 8. Display Flashcards (if any)
if st.session_state.flashcards:
    st.header("Flashcards")

    # Show "Card X of Y"
    total_cards = len(st.session_state.flashcards)
    current_idx = st.session_state.current_index

    st.write(f"**Card {current_idx + 1} of {total_cards}**")
    st.progress((current_idx + 1) / total_cards)

    current_flashcard = st.session_state.flashcards[current_idx]

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

        # 9. Navigation Buttons Using on_click Callbacks
        col_left, col_spacer, col_right = st.columns([3, 10, 3])
        with col_left:
            st.button("⬅️ Previous", on_click=go_to_previous_card)
        with col_right:
            st.button("Next ➡️", on_click=go_to_next_card)
