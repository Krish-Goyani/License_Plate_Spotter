import streamlit as st
from main import DetectLicensePlate
from utils.fetch_user_data import FetchUserData
import time


detect_license_plate = DetectLicensePlate()
fetch_user_data = FetchUserData()

def main():
    st.set_page_config(page_title="PlateGuard", page_icon="🚗", layout="wide")

    # Custom CSS for animations and styling
    st.markdown("""
    <style>
    .big-font {
        font-size: 24px !important;
    }
    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }
    .fade-in {
        animation: fadeIn 3s;
    }
    .pulsate {
        animation: pulsate 3s infinite;
    }
    @keyframes pulsate {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }
    </style>
    """, unsafe_allow_html=True)

    # Title and subtitle with animation
    st.markdown('<h2 class="fade-in">🚗 PlateGuard: Smart License Plate Recognition System</h2>', unsafe_allow_html=True)
    st.markdown('<h4 class="fade-in">📸 Effortlessly Detect License Plates and Retrieve User Data</h4>', unsafe_allow_html=True)

    # Project information
    st.markdown("""
    ### About PlateGuard 🛡️
    PlateGuard is a license plate recognition system that combines computer vision 
    and database integration to provide quick and accurate vehicle information. 
    Our system can:
    - 🔍 Detect license plates from video input
    - 🔢 Recognize and extract license plate numbers
    - 💾 Fetch associated user data from the database
    - 📊 Display results in a user-friendly interface
    
    Perfect for parking management, security systems, and traffic monitoring!
    """)

    # File uploader for video with pulsating effect
    st.markdown('<div class="pulsate">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a video file 🎥", type=["mp4", "avi", "mov"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with open("uploaded_video.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Process the video with a progress bar
        with st.spinner('Processing video... 🔄'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.4)  # Simulate processing time
                progress_bar.progress(i + 1)
            csv_file_path = detect_license_plate.detect_license_plate("uploaded_video.mp4")

        st.success('Video processed successfully! ✅')

        # Fetch and display user data
        user_data = fetch_user_data.fetch_user_data(csv_file_path)
        st.subheader("📋 User Information")
        st.table(user_data)

    # Additional information and styling in sidebar
    st.sidebar.markdown('<h4 class="big-font">🚀 PlateGuard Features</h4>', unsafe_allow_html=True)
    st.sidebar.markdown("""
    - ⚡ Real-time License Plate Detection
    - 🎯 High Accuracy Recognition
    - 🔍 Instant Database Query
    - 😊 User-friendly Interface
    """)

    st.sidebar.markdown("---")
    st.sidebar.markdown('<h4 class="big-font">📬 Contact Information</h4>', unsafe_allow_html=True)
    st.sidebar.markdown("""
    👤 <a href="https://www.datascienceportfol.io/Krish_Goyani" target="_blank" class="sidebar-link">Krish Goyani</a>
    
    📧 [Email](mailto:krishhgoyanii@gmail.com)
    
    🔗 <a href="https://www.linkedin.com/in/krish-goyani/" target="_blank" class="sidebar-link">LinkedIn</a>
    
    💻 <a href="https://github.com/Krish-Goyani" target="_blank" class="sidebar-link">GitHub</a>

    """, unsafe_allow_html=True)



    # Footer
    st.markdown("---")
    st.markdown("© 2024 PlateGuard. All rights reserved. 🔒")

if __name__ == "__main__":
    main()