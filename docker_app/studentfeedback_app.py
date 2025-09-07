import streamlit as st
import boto3
import json
import uuid
from datetime import datetime
import time
import os

# Set page config
st.set_page_config(page_title="Texas A&M Student Feedback Form", layout="wide")

# Custom theme for Texas A&M
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Work+Sans:wght@400;700&family=Open+Sans:wght@400;700&display=swap');
    
    .reportview-container {
        background-color: #FFFFFF;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    h1, h2, h3 {
        font-family: 'Oswald', sans-serif;
        color: #500000;
    }
    body {
        font-family: 'Open Sans', sans-serif;
        color: #333333;
    }
    .stButton > button {
        background-color: #500000;
        color: white;
        font-family: 'Work Sans', sans-serif;
    }
    .stSelectbox, .stSlider, .stTextInput, .stTextArea {
        font-family: 'Open Sans', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #F1F1F1;
    }
</style>
""", unsafe_allow_html=True)

# Set up S3 client using environment variables
s3 = boto3.client('s3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_DEFAULT_REGION')
)

# Get S3 bucket name from environment variable
S3_BUCKET_NAME = "awsbin-amazonq-assets"

# Header
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("./primaryTAM.png", width=300)
st.title("Student Feedback Form")
st.write("Your opinion matters! Help us improve our programs.")

# Main form
with st.form("feedback_form"):
    student_id = str(uuid.uuid4())[:8]  # Generate anonymized ID
    st.write(f"Your anonymized Student ID: {student_id}")

    program_name = st.text_input("Program Name", help="Enter the full name of your academic program")
    
    course_satisfaction = st.slider("Course Satisfaction", 1, 5, 3, help="Rate your overall satisfaction with the course")
    st.write("1: Very Dissatisfied, 5: Very Satisfied")
    
    learning_outcomes = st.slider("Learning Outcomes Achievement", 1, 5, 3, help="How well did the course meet its stated learning objectives?")
    
    support_services = st.slider("Support Services Rating", 1, 5, 3, help="Rate the quality of support services provided")
    
    engagement_level = st.select_slider("Engagement Level", options=["Low", "Medium", "High"], value="Medium", help="How engaged were you in the course activities?")
    
    improvement_areas = st.multiselect("Areas for Improvement", 
        ["Course Content", "Teaching Methods", "Assessment", "Resources", "Support Services"],
        help="Select all areas where you think improvements can be made")
    
    feedback = st.text_area("Open-ended Feedback", help="Please provide any additional comments or suggestions")
    
    future_plans = st.selectbox("Future Plans", ["Continue", "Transfer", "Undecided"], help="What are your plans for the next academic term?")

    with st.expander("Additional Comments"):
        strengths = st.text_area("Program Strengths", help="What aspects of the program do you find most valuable?")
        weaknesses = st.text_area("Areas for Enhancement", help="What aspects of the program could be improved?")

    submitted = st.form_submit_button("Submit Feedback")

if submitted:
    if not program_name:
        st.error("Please enter your program name.")
    elif not feedback:
        st.error("Please provide some feedback in the open-ended section.")
    else:
        feedback_data = {
            "Student ID": student_id,
            "Program Name": program_name,
            "Course Satisfaction": course_satisfaction,
            "Learning Outcomes Achievement": learning_outcomes,
            "Support Services Rating": support_services,
            "Engagement Level": engagement_level,
            "Areas for Improvement": improvement_areas,
            "Open-ended Feedback": feedback,
            "Future Plans": future_plans,
            "Program Strengths": strengths,
            "Areas for Enhancement": weaknesses,
            "Timestamp": datetime.now().isoformat()
        }

        # Convert data to JSON string
        feedback_json = json.dumps(feedback_data)

        # Generate a unique filename
        filename = f"feedback_{student_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

        try:
            # Show progress bar
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)

            # Upload to S3
            s3.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=filename,
                Body=feedback_json
            )
            st.success("Thank you! Your feedback has been submitted successfully.")
            st.balloons()
        except Exception as e:
            st.error(f"An error occurred while saving your feedback: {str(e)}")

# Sidebar
st.sidebar.title("Frequently Asked Questions")
faq_expander = st.sidebar.expander("Why is this feedback important?")
with faq_expander:
    st.write("Your feedback helps us continuously improve our programs and enhance the learning experience for all Aggies.")

st.sidebar.info("Your responses are anonymous and will be used solely for program improvement purposes.")

# Data privacy notice
st.sidebar.markdown("---")
st.sidebar.subheader("Data Privacy Notice")
st.sidebar.write("""
We value your privacy. All responses are anonymized and securely stored. 
The data collected will only be used for program improvement purposes and will not be shared with third parties.
""")

# Footer
st.markdown("---")
st.markdown("© 2025 Texas A&M University. All rights reserved.")
