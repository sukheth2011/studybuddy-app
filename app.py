import streamlit as st
from datetime import date, date, timedelta
import google.generativeai as genai
import os

# Configure Gemini API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
st.set_page_config(page_title="StudyBuddy AI", layout="wide", page_icon="📚")

# Login System
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['show_signup'] = False
    if 'registered_users' not in st.session_state:
        st.session_state['registered_users'] = {'student': 'study123', 'demo': 'demo123'}

def check_credentials(username, password):
    # Simple authentication - you can enhance this
    return st.session_state['registered_users'].get(username) == password

if not st.session_state['logged_in']:
    st.markdown('<p class="main-header">📚 StudyBuddy AI Login</p>', unsafe_allow_html=True)
    st.write("**Welcome! Please login to access your study dashboard**")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### 🔐 Login")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 Login", use_container_width=True):
                if check_credentials(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        
        with col_btn2:
            if st.button("📝 Demo Login", use_container_width=True):
                st.session_state['logged_in'] = True
                st.session_state['username'] = 'demo'
                st.success("Logged in as demo user!")
                st.rerun()
        
        st.info("💡 **Demo Credentials:** username: `demo` password: `demo123`")
        st.info("💡 **Student Login:** username: `student` password: `study123`")

    # Toggle between login and signup
    st.markdown("---")
    if not st.session_state['show_signup']:
        if st.button("✨ Create New Account"):
            st.session_state['show_signup'] = True
            st.rerun()
    else:
        st.markdown("### 📝 Create Your Account")
        with st.form("signup_form"):
            new_username = st.text_input("👤 Choose Username", placeholder="Enter a username")
            new_password = st.text_input("🔒 Choose Password", type="password", placeholder="Enter a password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            
            col1, col2 = st.columns(2)
            with col1:
                signup_button = st.form_submit_button("🚀 Sign Up")
            with col2:
                back_button = st.form_submit_button("← Back to Login")
            
            if signup_button:
                if not new_username or not new_password:
                    st.error("❌ Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("❌ Passwords don't match!")
                elif new_username in st.session_state['registered_users']:
                    st.error("❌ Username already exists!")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    # Register the new user
                    st.session_state['registered_users'][new_username] = new_password
                    st.success(f"✅ Account created successfully! Welcome {new_username}!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = new_username
                    st.session_state['show_signup'] = False
                    st.rerun()
            
            if back_button:
                st.session_state['show_signup'] = False
                st.rerun()
    
    st.stop()

# Custom CSS
st.markdown("""
<style>
.main-header {font-size: 2.5rem; color: #4CAF50; font-weight: bold;}
.sub-header {font-size: 1.5rem; color: #2196F3;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📚 StudyBuddy AI: Your Smart Study Companion</p>', unsafe_allow_html=True)
st.write("**Powered by AI - Get instant answers to homework, exam prep & study questions!**")

# User info in sidebar
st.sidebar.success(f"👤 Logged in as: **{st.session_state['username']}**")
if st.sidebar.button("🚪 Logout"):
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.rerun()

# Sidebar Navigation
menu = st.sidebar.radio("Navigate", ["📚 Dashboard", "📝 AI Homework Helper", "📋 To-Do List", "📅 Exam Countdown", "🗒️ Notes", "🎴 Flashcards", "📖 Resources"])

# Dashboard
if menu == "📚 Dashboard":
    st.markdown('<p class="sub-header">Welcome to StudyBuddy AI!</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("✅ AI-Powered Answers")
    with col2:
        st.info("📊 Track Progress")
    with col3:
        st.info("⚡ Quick Study Tools")
    st.write("### Quick Stats")
    tasks = st.session_state.get("tasks", [])
    completed = len([t for t in tasks if t.get("done")])
    st.metric("Tasks Completed", completed)

# AI Homework Helper
elif menu == "📝 AI Homework Helper":
    st.markdown('<p class="sub-header">AI Homework & Question Solver</p>', unsafe_allow_html=True)
    st.write("Ask any homework question, get explanations, solve math problems, and more!")
    
    subject = st.selectbox("Select Subject", ["Math", "Science", "English", "History", "Geography", "Physics", "Chemistry", "Biology"])
    question = st.text_area("Enter your question or homework problem:", height=150)
    
    if st.button("🚀 Get AI Answer"):
        if question:
            with st.spinner("🤔 AI is thinking..."):
                try:
                    prompt = f"You are a helpful tutor for high school students. Subject: {subject}. Question: {question}"
                    response = model.generate_content(prompt)
                    st.success("✅ Answer:")
                    st.write(response.text)
                except Exception as e:
                    st.error("Error: " + str(e))
        else:
                st.warning("Please enter a question!")

# To-Do List
elif menu == "📋 To-Do List":
    st.markdown('<p class="sub-header">Homework & Task Tracker</p>', unsafe_allow_html=True)
    if "tasks" not in st.session_state:
        st.session_state["tasks"] = []
    
    col1, col2 = st.columns([3, 1])
    with col1:
        new_task = st.text_input("Add a new task")
    with col2:
        priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"])
    
    if st.button("➕ Add Task") and new_task:
        st.session_state["tasks"].append({"task": new_task, "done": False, "priority": priority})
    
    st.write("### Your Tasks")
    for idx, t in enumerate(st.session_state["tasks"]):
        col1, col2, col3 = st.columns([0.5, 3, 1])
        with col1:
            done = st.checkbox("", value=t["done"], key=f"task_{idx}")
            st.session_state["tasks"][idx]["done"] = done
        with col2:
            if done:
                st.write(f"~~{t['priority']} {t['task']}~~")
            else:
                st.write(f"{t['priority']} {t['task']}")
        with col3:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state["tasks"].pop(idx)
                st.rerun()

# Exam Countdown
elif menu == "📅 Exam Countdown":
    st.markdown('<p class="sub-header">Exam Countdown Timer</p>', unsafe_allow_html=True)
    if "exams" not in st.session_state:
        st.session_state["exams"] = []
    
    col1, col2 = st.columns(2)
    with col1:
        exam_name = st.text_input("Exam Name")
    with col2:
        exam_date = st.date_input("Exam Date", value=date.today()+timedelta(days=7))
    
    if st.button("➕ Add Exam"):
        st.session_state["exams"].append({"name": exam_name, "date": exam_date})
    
    st.write("### Upcoming Exams")
    for exam in st.session_state["exams"]:
        days_left = (exam["date"] - date.today()).days
        if days_left >= 0:
            st.info(f"***{exam['name']}** - {days_left} days left! ({exam['date']})")
        else:
            st.success(f"***{exam['name']}** - Completed")

# Notes
elif menu == "🗒️ Notes":
    st.markdown('<p class="sub-header">Subject Notes</p>', unsafe_allow_html=True)
        
    st.markdown("### 🤖 Generate AI Notes")
    chapter_topic = st.text_input("📝 Enter chapter name or topic:")
    subject = st.selectbox("Subject:", ["Math", "Science", "English", "History", "Physics", "Chemistry", "Biology"])
    
    if st.button("🚀 Generate Notes"):
        if chapter_topic:
            with st.spinner("Generating comprehensive notes..."):
                try:
                    prompt = f"""Create comprehensive study notes for a 9th grade {subject} student on the topic: {chapter_topic}.
                    
                    Include:
                    1. Key Concepts and Definitions
                    2. Important Points to Remember
                    3. Examples
                    4. Common Mistakes to Avoid
                    5. Quick Tips for Exam Preparation
                    
                    Make it clear, concise, and easy to understand."""
                    
                    response = model.generate_content(prompt)
                    st.success("✅ Notes Generated!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    if "all_notes" not in st.session_state:
                        st.session_state["all_notes"] = []
                    st.session_state["all_notes"].append({"subject": subject, "topic": chapter_topic, "notes": response.text, "date": date.today()})
                    st.info("💾 Notes saved to 'Saved Notes' section below!")
                except:
                    st.error("Error generating notes. Please try again.")
        else:
            st.warning("Please enter a chapter or topic name!")
    
    st.markdown("---")
    if "all_notes" not in st.session_state:
        st.session_state["all_notes"] = []
    
    note_subject = st.selectbox("Subject", ["Math", "Science", "English", "History", "Physics", "Chemistry", "Biology"])
    note = st.text_area("Write your notes here...", height=200)
    
    if st.button("📝 Save Note"):
        st.session_state["all_notes"].append({"subject": note_subject, "note": note, "date": date.today()})
        st.success("Note saved!")
    
    st.write("### Saved Notes")
    for n in st.session_state["all_notes"]:
        with st.expander(f"📚 {n['subject']} - {n['date']}"):
            st.write(n["note"])

# Flashcards
elif menu == "🎴 Flashcards":
    st.markdown('<p class="sub-header">Study Flashcards</p>', unsafe_allow_html=True)
        
    st.markdown("### 🤖 Generate AI Flashcards")
    chapter_topic = st.text_input("📝 Enter chapter name or topic:", key="flashcard_topic")
    subject = st.selectbox("Subject:", ["Math", "Science", "English", "History", "Physics", "Chemistry", "Biology"], key="flashcard_subject")
    num_cards = st.slider("Number of flashcards:", 5, 20, 10)
    
    if st.button("🚀 Generate Flashcards"):
        if chapter_topic:
            with st.spinner(f"Generating {num_cards} flashcards..."):
                try:
                    prompt = f"""Create exactly {num_cards} study flashcards for a 9th grade {subject} student on the topic: {chapter_topic}.
                    
                    Format each flashcard as:
                    Q: [Question]
                    A: [Answer]
                    
                    Make questions clear and concise. Keep answers brief but complete.
                    Cover the most important concepts."""
                    
                    response = model.generate_content(prompt)
                    flashcards_text = response.text
                    
                    cards = []
                    lines = flashcards_text.split('\n')
                    current_q = ""
                    current_a = ""
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('Q:'):
                            if current_q and current_a:
                                cards.append({"q": current_q, "a": current_a})
                            current_q = line[2:].strip()
                            current_a = ""
                        elif line.startswith('A:'):
                            current_a = line[2:].strip()
                    
                    if current_q and current_a:
                        cards.append({"q": current_q, "a": current_a})
                    
                    if cards:
                        if "flashcards" not in st.session_state:
                            st.session_state["flashcards"] = []
                        st.session_state["flashcards"].extend(cards)
                        
                        st.success(f"✅ Generated {len(cards)} flashcards!")
                        st.info("👇 Scroll down to 'Your Flashcards' to study them!")
                    else:
                        st.error("Could not parse flashcards. Please try again.")
                except Exception as e:
                    st.error(f"Error generating flashcards: {str(e)}")
        else:
            st.warning("Please enter a chapter or topic name!")
    
    st.markdown("---")
    if "flashcards" not in st.session_state:
        st.session_state["flashcards"] = []
    
    col1, col2 = st.columns(2)
    with col1:
        question = st.text_input("Question")
    with col2:
        answer = st.text_input("Answer")
    
    if st.button("➕ Add Flashcard"):
        st.session_state["flashcards"].append({"q": question, "a": answer})
    
    st.write("### Your Flashcards")
    for idx, fc in enumerate(st.session_state["flashcards"]):
        with st.expander(f"❓ {fc['q']}"):
            st.success(f"✅ {fc['a']}")

# Resources
elif menu == "📖 Resources":
    st.markdown('<p class="sub-header">Quick Study Resources</p>', unsafe_allow_html=True)
    st.markdown("""
    ### 📚 Learning Platforms
    - [Khan Academy](https://www.khanacademy.org/) - Free courses
    - [NCERT Books](https://ncert.nic.in/textbook.php) - Indian curriculum
    - [BBC Bitesize](https://www.bbc.co.uk/bitesize) - UK curriculum
    
    ### 🧮 Tools
    - [Wolfram Alpha](https://www.wolframalpha.com/) - Math solver
    - [Quizlet](https://quizlet.com/) - Flashcards
    - [Grammarly](https://www.grammarly.com/) - Writing help
    
    ### 🎥 Video Learning
    - [YouTube Edu](https://www.youtube.com/education)
    - [CrashCourse](https://thecrashcourse.com/)
    """)
    
    st.sidebar.info("💡 **Tip:** Use AI Helper for instant answers!")
    st.sidebar.success("🚀 Powered by Gemini AI & Python")
