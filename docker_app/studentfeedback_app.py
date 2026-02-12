import streamlit as st
import boto3
import json
import uuid
from datetime import datetime
import time
import os

from constants.ui_strings import (
    STUDENT_PAGE_TITLE,
    STUDENT_TITLE,
    STUDENT_DESCRIPTION,
    STUDENT_ID_TEXT,
    STUDENT_LABEL_PROGRAM_NAME,
    STUDENT_HELP_PROGRAM_NAME,
    STUDENT_LABEL_COURSE_SATISFACTION,
    STUDENT_HELP_COURSE_SATISFACTION,
    STUDENT_SATISFACTION_SCALE_TEXT,
    STUDENT_LABEL_LEARNING_OUTCOMES,
    STUDENT_HELP_LEARNING_OUTCOMES,
    STUDENT_LABEL_SUPPORT_SERVICES,
    STUDENT_HELP_SUPPORT_SERVICES,
    STUDENT_LABEL_ENGAGEMENT_LEVEL,
    STUDENT_HELP_ENGAGEMENT_LEVEL,
    STUDENT_ENGAGEMENT_OPTIONS,
    STUDENT_ENGAGEMENT_DEFAULT,
    STUDENT_LABEL_IMPROVEMENT_AREAS,
    STUDENT_HELP_IMPROVEMENT_AREAS,
    STUDENT_IMPROVEMENT_AREA_OPTIONS,
    STUDENT_LABEL_OPEN_FEEDBACK,
    STUDENT_HELP_OPEN_FEEDBACK,
    STUDENT_LABEL_FUTURE_PLANS,
    STUDENT_HELP_FUTURE_PLANS,
    STUDENT_FUTURE_PLANS_OPTIONS,
    STUDENT_EXPANDER_ADDITIONAL_COMMENTS,
    STUDENT_LABEL_STRENGTHS,
    STUDENT_HELP_STRENGTHS,
    STUDENT_LABEL_WEAKNESSES,
    STUDENT_HELP_WEAKNESSES,
    STUDENT_BUTTON_SUBMIT,
    STUDENT_ERROR_PROGRAM_NAME_REQUIRED,
    STUDENT_ERROR_FEEDBACK_REQUIRED,
    STUDENT_SUCCESS_SUBMITTED,
    STUDENT_ERROR_SAVE_FAILED,
    STUDENT_SIDEBAR_TITLE,
    STUDENT_FAQ_EXPANDER_TITLE,
    STUDENT_FAQ_ANSWER,
    STUDENT_SIDEBAR_INFO,
    STUDENT_SIDEBAR_PRIVACY_TITLE,
    STUDENT_SIDEBAR_PRIVACY_TEXT,
    STUDENT_FOOTER_TEXT,
)

# Set page config
st.set_page_config(page_title=STUDENT_PAGE_TITLE, layout="wide")

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
st.title(STUDENT_TITLE)
st.write(STUDENT_DESCRIPTION)

# Main form
with st.form("feedback_form"):
    student_id = str(uuid.uuid4())[:8]  # Generate anonymized ID
    st.write(STUDENT_ID_TEXT.format(student_id=student_id))

    program_name = st.text_input(STUDENT_LABEL_PROGRAM_NAME, help=STUDENT_HELP_PROGRAM_NAME)
    
    course_satisfaction = st.slider(STUDENT_LABEL_COURSE_SATISFACTION, 1, 5, 3, help=STUDENT_HELP_COURSE_SATISFACTION)
    st.write(STUDENT_SATISFACTION_SCALE_TEXT)
    
    learning_outcomes = st.slider(STUDENT_LABEL_LEARNING_OUTCOMES, 1, 5, 3, help=STUDENT_HELP_LEARNING_OUTCOMES)
    
    support_services = st.slider(STUDENT_LABEL_SUPPORT_SERVICES, 1, 5, 3, help=STUDENT_HELP_SUPPORT_SERVICES)
    
    engagement_level = st.select_slider(STUDENT_LABEL_ENGAGEMENT_LEVEL, options=STUDENT_ENGAGEMENT_OPTIONS, value=STUDENT_ENGAGEMENT_DEFAULT, help=STUDENT_HELP_ENGAGEMENT_LEVEL)
    
    improvement_areas = st.multiselect(STUDENT_LABEL_IMPROVEMENT_AREAS, 
        STUDENT_IMPROVEMENT_AREA_OPTIONS,
        help=STUDENT_HELP_IMPROVEMENT_AREAS)
    
    feedback = st.text_area(STUDENT_LABEL_OPEN_FEEDBACK, help=STUDENT_HELP_OPEN_FEEDBACK)
    
    future_plans = st.selectbox(STUDENT_LABEL_FUTURE_PLANS, STUDENT_FUTURE_PLANS_OPTIONS, help=STUDENT_HELP_FUTURE_PLANS)

    with st.expander(STUDENT_EXPANDER_ADDITIONAL_COMMENTS):
        strengths = st.text_area(STUDENT_LABEL_STRENGTHS, help=STUDENT_HELP_STRENGTHS)
        weaknesses = st.text_area(STUDENT_LABEL_WEAKNESSES, help=STUDENT_HELP_WEAKNESSES)

    submitted = st.form_submit_button(STUDENT_BUTTON_SUBMIT)

if submitted:
    if not program_name:
        st.error(STUDENT_ERROR_PROGRAM_NAME_REQUIRED)
    elif not feedback:
        st.error(STUDENT_ERROR_FEEDBACK_REQUIRED)
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
            st.success(STUDENT_SUCCESS_SUBMITTED)
            st.balloons()
        except Exception as e:
            st.error(STUDENT_ERROR_SAVE_FAILED.format(error=str(e)))

# Sidebar
st.sidebar.title(STUDENT_SIDEBAR_TITLE)
faq_expander = st.sidebar.expander(STUDENT_FAQ_EXPANDER_TITLE)
with faq_expander:
    st.write(STUDENT_FAQ_ANSWER)

st.sidebar.info(STUDENT_SIDEBAR_INFO)

# Data privacy notice
st.sidebar.markdown("---")
st.sidebar.subheader(STUDENT_SIDEBAR_PRIVACY_TITLE)
st.sidebar.write(STUDENT_SIDEBAR_PRIVACY_TEXT)

# Footer
st.markdown("---")
st.markdown(STUDENT_FOOTER_TEXT)
