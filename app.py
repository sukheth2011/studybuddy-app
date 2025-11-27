import streamlit as st
from datetime import date, timedelta
import google.generativeai as genai
import os
import time

# Configure Gemini API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
st.set_page_config(page_title="StudyBuddy AI", layout="wide", page_icon="📚")

# Custom CSS for colorful and beautiful design
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: #f5f5f5;
                color: #000000;
                            border-top: 10px solid #000000;
                                        border-bottom: 10px solid #000000;
                                                    border-left: 10px solid #000000;
                                                                border-right: 10px solid #000000;
                                                                            padding: 20px;
                                                                                        border-radius: 50px;
                                                                                                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                                                                                                                max-width: 1200px;
                                                                                                                            margin: 0 auto;
    }

        /* Input fields and text areas with black borders */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border: 1px solid #000000 !important;
        color: #000000 !important;
                border-radius: 50px !important;
                        padding: 15px !important;
                                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
                                        font-size: 16px !important;
    }
    
    /* Buttons with black borders */
    .stButton > button {
        border: 1px solid #000000 !important;
        color: #000000 !important;
                border-radius: 50px !important;
                        padding: 12px 30px !important;
                                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
                                        font-size: 16px !important;
                                                font-weight: 600 !important;
                                                        transition: all 0.3s ease !important;

                                                            /* Button hover effects */
                                                                .stButton > button:hover {
                                                                        transform: translateY(-2px) !important;
                                                                                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3) !important;
                                                                                        background-color: #0056b3 !important;
                                                                                            }
    }
    
    /* Tab containers with black borders */
    .stTabs {
        border-bottom: 1px solid #000000 !important;
                border-radius: 50px 10px 0 0 !important;
                        padding: 10px 20px !important;
                                box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15) !important;
                                        font-weight: 600 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Login/Signup container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Text styling */
    h1, h2, h3 {
        color: #000000 !important;
            font-weight: 700 !important;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
                    margin-bottom: 20px !important;
    }
    
    p {
        color: #000000 !important;
    
    /* Input fields styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #fff !important;
        border-radius: 50px !important;
        padding: 12px !important;
        font-size: 16px !important;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1) !important;
        color: #333 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important;
        transform: scale(1.02);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 30px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 20px rgba(245, 87, 108, 0.4) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(245, 87, 108, 0.6) !important;
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%) !important;
    }
    
    /* Info boxes styling */
    .stAlert {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%) !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 15px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%) !important;
        color: #155724 !important;
        border-radius: 50px !important;
        padding: 15px !important;
        font-weight: 600 !important;
        animation: slideIn 0.5s ease-out;
    }
    
    /* Error message */
    .stError {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important;
        color: #721c24 !important;
        border-radius: 50px !important;
        padding: 15px !important;
        font-weight: 600 !important;
        animation: shake 0.5s ease-out;
    }
    
    /* Info box custom styling */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Horizontal line */
    hr {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #fff, transparent);
        margin: 30px 0;
    }
    
    /* Animation for success */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Animation for error */
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Form container */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 50px !important;
        padding: 30px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3) !important;
    }
    
    /* Labels */
    .stTextInput > label, .stSelectbox > label {
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# Login System
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['show_signup'] = False
        st.session_state['subscription_tier'] = 'free'  # free or premium
        st.session_state['daily_queries'] = 0
    st.session_state['last_query_date'] = date.today()
    if 'registered_users' not in st.session_state:
        st.session_state['registered_users'] = {'student': 'study123', 'demo': 'demo123'}
def check_credentials(username, password):
    # Simple authentication - you can enhance this
    return st.session_state['registered_users'].get(username) == password


# Show signup form if user clicked CREATE NEW ACCOUNT
if st.session_state.get('show_signup', False):
        st.markdown('<p class="main-header">📚 Create New Account</p>', unsafe_allow_html=True)
        st.write("**Fill in the details to create your study account**")
    
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("### ✨ Sign Up")
            new_username = st.text_input("Choose Username", placeholder="Enter a username", key="new_user")
            new_password = st.text_input("Choose Password", type="password", placeholder="Enter a password", key="new_pass")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password", key="confirm_pass")
            
            col_signup, col_back = st.columns(2)
            with col_signup:
                if st.button("🎉 Create Account", use_container_width=True):
                    if new_password != confirm_password:
                        st.error("❌ Passwords don't match!")
                    elif new_username in st.session_state['registered_users']:
                        st.error("❌ Username already exists!")
                    elif len(new_username) < 3 or len(new_password) < 6:
                        st.error("❌ Username must be 3+ chars, password must be 6+ chars!")
                    else:
                        st.session_state['registered_users'][new_username] = new_password
                        st.success(f"✅ Account created for {new_username}! You can now login.")
                        st.session_state['show_signup'] = False
                        st.rerun()
            
            with col_back:
                if st.button("◀️ Back to Login", use_container_width=True):
                    st.session_state['show_signup'] = False
                    st.rerun()

elif not st.session_state['logged_in']:
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
            if st.button("👤 Guest Login", use_container_width=True):
                st.session_state['logged_in'] = True
                st.session_state['username'] = 'guest'
                st.session_state['guest_login_time'] = time.time()
                st.success("Logged in as guest user! Session will expire in 5 minutes.")
                st.rerun()

    # Create new account button
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("✨ CREATE NEW ACCOUNT", use_container_width=True, key="signup_btn"):
        st.session_state['show_signup'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Main App (After successful login)
else:
    # Check if guest session has expired
    if st.session_state['username'] == 'guest' and 'guest_login_time' in st.session_state:
        elapsed_time = time.time() - st.session_state['guest_login_time']
        if elapsed_time >= 300:  # 5 minutes = 300 seconds
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.session_state.pop('guest_login_time', None)
            st.warning("Guest session expired. Please login again.")
            st.rerun()

    # Display remaining time for guest users
    if st.session_state['username'] == 'guest' and 'guest_login_time' in st.session_state:
        elapsed_time = time.time() - st.session_state['guest_login_time']
        remaining_seconds = max(0, 300 - int(elapsed_time))
        remaining_minutes = remaining_seconds // 60
        remaining_secs = remaining_seconds % 60
        st.warning(f"⏰ Guest Session - Time Remaining: {remaining_minutes}:{remaining_secs:02d} minutes")

    # StudyBuddy AI Dashboard
    st.markdown(f"### 👋 Welcome, {st.session_state['username']}!")
    st.markdown("---")
    
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Chat", "📚 Homework Help", "📖 Exam Prep", "💎 Premium"])    
    with tab1:
        st.markdown("### 🤖 AI Study Assistant")
        st.write("Ask me anything about your studies!")
        
        # Initialize chat history
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []
        
        # Display chat history
        for message in st.session_state['chat_history']:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**StudyBuddy:** {message['content']}")
        
        # Chat input
        user_question = st.text_input("Ask your question:", key="chat_input")
        
        if st.button("📤 Send", key="send_btn"):
            if user_question:
                # Add user message
                st.session_state['chat_history'].append({'role': 'user', 'content': user_question})
                
                # Get AI response
                try:
                    response = model.generate_content(f"You are a helpful study assistant for high school students. Answer this question clearly and concisely: {user_question}")
                    ai_response = response.text
                    st.session_state['chat_history'].append({'role': 'assistant', 'content': ai_response})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.markdown("### 📝 Homework Help")
        st.write("Get help with your homework!")
        
        subject = st.selectbox("Select Subject:", ["Math", "Physics", "Chemistry", "Biology", "English", "History", "Other"])
        
        homework_question = st.text_area("Describe your homework problem:", height=150)
        
        if st.button("💡 Get Help", key="homework_btn"):
            if homework_question:
                with st.spinner("Thinking..."):
                    try:
                        prompt = f"You are a helpful tutor. Help this high school student with their {subject} homework. Explain step-by-step:\n\n{homework_question}"
                        response = model.generate_content(prompt)
                        st.success("✅ Here's your solution:")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please describe your homework problem first!")
    
    with tab3:
        st.markdown("### 🎯 Exam Preparation")
        st.write("Prepare for your exams with practice questions!")
        
        exam_subject = st.selectbox("Select Subject:", ["Math", "Physics", "Chemistry", "Biology", "English", "History"], key="exam_subject")
        
        topic = st.text_input("Enter topic to study:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Generate Practice Questions"):
                if topic:
                    with st.spinner("Generating questions..."):
                        try:
                            prompt = f"Generate 5 practice questions for high school {exam_subject} on the topic: {topic}. Include a mix of easy, medium, and hard questions."
                            response = model.generate_content(prompt)
                            st.success("✅ Practice Questions:")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please enter a topic!")
        
        with col2:
            if st.button("📖 Get Study Summary"):
                if topic:
                    with st.spinner("Creating summary..."):
                        try:
                            prompt = f"Create a concise study summary for high school {exam_subject} on the topic: {topic}. Include key concepts and important points."
                            response = model.generate_content(prompt)
                            st.success("✅ Study Summary:")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("Please enter a topic!")
    
    # Premium Tab
    with tab4:
                st.markdown("💎 **Upgrade to Premium**")
                st.write("Unlock unlimited access to all features!")

        col1, col2 = st.columns(2)

        with col1:
                        st.markdown("### 🆓 Free Tier")
                        st.write("✅ 10 questions per day")
                        st.write("✅ Basic AI features")
                        st.write("❌ Limited homework help")
                        st.write("❌ Ads supported")

        with col2:
                        st.markdown("### 💎 Premium Tier")
                        st.write("✅ **Unlimited questions**")
                        st.write("✅ **Advanced AI features**")
                        st.write("✅ **Priority support**")
                        st.write("✅ **No ads**")
                        st.write("")
                        st.markdown("**💵 ₹299/month or ₹2999/year**")

        st.markdown("---")

        if st.button("💎 Upgrade to Premium", key="upgrade_btn"):
                        st.session_state['subscription_tier'] = 'premium'
                        st.success("🎉 Welcome to Premium! You now have unlimited access to all features!")
                        st.balloons()


# Logout button
    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        if 'chat_history' in st.session_state:
            del st.session_state['chat_history']
        st.rerun()
