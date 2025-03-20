# :sparkles: Let's-Learn: AI Flashcard Generator :sparkles:

**Welcome to the Lets-Learn project!** This app uses CrewAI to automatically generate flashcards for any topic, providing a fun and interactive way to study. Below is the **Task Progress Manager** to keep track of features and improvements.

---

## :bookmark_tabs: Project Overview

- **Frontend**: [Streamlit](https://streamlit.io/)  
- **Backend**: [CrewAI](https://crew.ai/) with LLM and Tavily integration  
- **Primary Goals**:
  1. AI-based flashcard generation  
  2. Personalized memory/spaced repetition  
  3. Session history & analytics  
  4. Polished user interface  

---

## :chart_with_upwards_trend: Task Progress Manager

### :white_check_mark: **Done**

1. **CrewAI Agent Pipeline Setup**  
   - [x] Create Planner Agent  
   - [x] Create Search Agent (Tavily integration)  
   - [x] Create Flashcard Agent

2. **Basic Streamlit Front-end**  
   - [x] Topic input field  
   - [x] “Generate Flashcards” button  
   - [x] Flip-card UI for question/answer

3. **Environment & Configuration**  
   - [x] Use `dotenv` for API keys (CrewAI, Tavily)  
   - [x] Create `requirements.txt`

---

### :hourglass_flowing_sand: **In Progress**

1. **Advanced Error Handling & Logging**  
   - [ ] Add robust `try/except` in flashcard generation  
   - [ ] Display fallback messages for LLM/Tool errors  
   - [ ] (Optional) Integrate an error-reporting tool (e.g., Sentry)

2. **Basic Scoring Mechanism**  
   - [ ] Prompt user for input before revealing correct answer  
   - [ ] Compare user input with correct answer & mark correct/incorrect  
   - [ ] Store correctness data in session state  
   - [ ] New scoring agent with memory
  
3. **UI/UX Improvements**  
   - [x] Add loading bar
   - [x] Add progress indicator (e.g., “Card X of Y”)  
   - [ ] Consider multi-page Streamlit layout (“Review Sessions,” “New Deck,” etc.)  
   - [ ] Refine styling, responsiveness, and instructions
   

---

### :dart: **To Do**

1. **Memory & Personalization (Spaced Repetition)**  
   - [ ] Implement spaced repetition algorithm (e.g., SM-2)  
   - [ ] Track user performance (right/wrong answers)  
   - [ ] Dynamically prioritize missed questions

2. **Session Recording & Review System**  
   - [ ] Integrate a database or file-based storage (memory within agents if needed)  
   - [ ] Record session info (timestamps, performance, user)  
   - [ ] Build UI page to review past sessions & retake flashcards

3. **Authentication**  
   - [ ] Sign up/login  
   - [ ] Store user data securely  
   - [ ] Ensure privacy integration (protect user info)

4. **UI/UX Improvements**  
   - [ ] Add progress indicator (e.g., “Card X of Y”)  
   - [ ] Consider multi-page Streamlit layout (“Review Sessions,” “New Deck,” etc.)  
   - [ ] Refine styling, responsiveness, and instructions
   - [ ] Add loading bar

5. **Testing & Deployment Strategy**  
   - [ ] Write unit tests (e.g., `pytest`)  
   - [ ] Add Continuous Integration (GitHub Actions, GitLab CI, etc.)  
   - [ ] Deploy (CrewAI backend + Streamlit app) on hosting platform

6. **Performance & Caching**  
   - [ ] Cache LLM/search results to reduce repeated API calls  
   - [ ] Optimize CrewAI calls & possibly add concurrency handling  
   - [ ] Profile for bottlenecks (time/memory usage)

---

## Notes
- CrewAI installation easiest with Python 3.12

## :tada: Thank You!

Thank you for checking out the Lets-Learn AI Flashcard Generator.

:rocket: **Happy Learning!**
