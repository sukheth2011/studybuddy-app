import streamlit as st
from datetime import date, date, timedelta
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
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
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    p {
        color: white !important;
    }
    
    /* Input fields styling */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #fff !important;
        border-radius: 15px !important;
        padding: 12px !important;
        font-size: 16px !important;
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
        border-radius: 25px !important;
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
        border-radius: 15px !important;
        border: none !important;
        padding: 15px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%) !important;
        color: #155724 !important;
        border-radius: 15px !important;
        padding: 15px !important;
        font-weight: 600 !important;
        animation: slideIn 0.5s ease-out;
    }
    
    /* Error message */
    .stError {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%) !important;
        color: #721c24 !important;
        border-radius: 15px !important;
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
        border-radius: 20px !important;
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
