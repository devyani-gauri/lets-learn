import streamlit as st
from backend import generate_flashcards

# Streamlit UI
st.title("📚 AI Flashcard Generator")
st.write("Generate AI-powered flashcards on any topic!")

# User input
topic = st.text_input("Enter a topic for flashcards:")

if st.button("Generate Flashcards"):
    if topic.strip():
        st.write("🔄 Generating flashcards, please wait...")
        
        # Call the CrewAI backend
        flashcards = generate_flashcards(topic)

        # Display flashcards
        st.write("## 📌 Generated Flashcards:")
        if isinstance(flashcards, list):  # ✅ Fix: Handle list format
            for flashcard in flashcards:
                if flashcard.startswith("Q:"):
                    st.markdown(f"**{flashcard}**")  # Bold for questions
                elif flashcard.startswith("A:"):
                    st.write(flashcard)  # Regular for answers
        else:
            st.write(flashcards)  # If something unexpected happens, show raw output
    else:
        st.warning("⚠️ Please enter a topic before generating flashcards.")