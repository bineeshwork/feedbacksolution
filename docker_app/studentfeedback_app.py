import streamlit as st
import boto3
import json
import uuid
from datetime import datetime
import time
import os

from constants.strings import (
    FEEDBACK_PAGE_TITLE,
    FEEDBACK_MAIN_TITLE,
    FEEDBACK_DESCRIPTION,
    FEEDBACK_ANONYMIZED_ID,
    FEEDBACK_LABEL_PROGRAM_NAME,
    FEEDBACK_HELP_PROGRAM_NAME,
    FEEDBACK_LABEL_COURSE_SATISFACTION,
    FEEDBACK_HELP_COURSE_SATISFACTION,
    FEEDBACK_SLIDER_SATISFACTION_DESCRIPTION,
    FEEDBACK_LABEL_LEARNING_OUTCOMES,
    FEEDBACK_HELP_LEARNING_OUTCOMES,
    FEEDBACK_LABEL_SUPPORT_SERVICES,
    FEEDBACK_HELP_SUPPORT_SERVICES,
    FEEDBACK_LABEL_ENGAGEMENT,
    FEEDBACK_HELP_ENGAGEMENT,
    FEEDBACK_ENGAGEMENT_OPTIONS,
    FEEDBACK_ENGAGEMENT_DEFAULT,
    FEEDBACK_LABEL_IMPROVEMENT_AREAS,
    FEEDBACK_HELP_IMPROVEMENT_AREAS,
    FEEDBACK_IMPROVEMENT_OPTIONS,
    FEEDBACK_LABEL_OPEN_FEEDBACK,
    FEEDBACK_HELP_OPEN_FEEDBACK,
    FEEDBACK_LABEL_FUTURE_PLANS,
    FEEDBACK_HELP_FUTURE_PLANS,
    FEEDBACK_FUTURE_PLANS_OPTIONS,
    FEEDBACK_LABEL_ADDITIONAL_COMMENTS,
    FEEDBACK_LABEL_STRENGTHS,
    FEEDBACK_HELP_STRENGTHS,
    FEEDBACK_LABEL_WEAKNESSES,
    FEEDBACK_HELP_WEAKNESSES,
    FEEDBACK_BUTTON_SUBMIT,
    FEEDBACK_ERROR_PROGRAM_NAME,
    FEEDBACK_ERROR_FEEDBACK_REQUIRED,
    FEEDBACK_SUCCESS_SUBMITTED,
    FEEDBACK_ERROR_SAVE_FAILED,
    FEEDBACK_SIDEBAR_FAQ_TITLE,
    FEEDBACK_SIDEBAR_FAQ_QUESTION,
    FEEDBACK_SIDEBAR_FAQ_ANSWER,
    FEEDBACK_SIDEBAR_INFO,
    FEEDBACK_SIDEBAR_PRIVACY_TITLE,
    FEEDBACK_SIDEBAR_PRIVACY_TEXT,
    FEEDBACK_FOOTER_COPYRIGHT,
)
from constants.config import (
    FEEDBACK_S3_BUCKET_NAME,
    FEEDBACK_LOGO_PATH,
    DEFAULT_AWS_REGION,
    ENABLE_BALLOONS,
    ENABLE_PROGRESS_BAR,
)

# Set page config
st.set_page_config(page_title=FEEDBACK_PAGE_TITLE, layout="wide")

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
    region_name=os.environ.get('AWS_DEFAULT_REGION', DEFAULT_AWS_REGION)
)

# Get S3 bucket name from environment variable (via config)
S3_BUCKET_NAME = FEEDBACK_S3_BUCKET_NAME

# Header
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(FEEDBACK_LOGO_PATH, width=300)
st.title(FEEDBACK_MAIN_TITLE)
st.write(FEEDBACK_DESCRIPTION)

# Main form
with st.form("feedback_form"):
    student_id = str(uuid.uuid4())[:8]  # Generate anonymized ID
    st.write(FEEDBACK_ANONYMIZED_ID.format(student_id=student_id))

    program_name = st.text_input(FEEDBACK_LABEL_PROGRAM_NAME, help=FEEDBACK_HELP_PROGRAM_NAME)
    
    course_satisfaction = st.slider(FEEDBACK_LABEL_COURSE_SATISFACTION, 1, 5, 3, help=FEEDBACK_HELP_COURSE_SATISFACTION)
    st.write(FEEDBACK_SLIDER_SATISFACTION_DESCRIPTION)
    
    learning_outcomes = st.slider(FEEDBACK_LABEL_LEARNING_OUTCOMES, 1, 5, 3, help=FEEDBACK_HELP_LEARNING_OUTCOMES)
    
    support_services = st.slider(FEEDBACK_LABEL_SUPPORT_SERVICES, 1, 5, 3, help=FEEDBACK_HELP_SUPPORT_SERVICES)
    
    engagement_level = st.select_slider(FEEDBACK_LABEL_ENGAGEMENT, options=FEEDBACK_ENGAGEMENT_OPTIONS, value=FEEDBACK_ENGAGEMENT_DEFAULT, help=FEEDBACK_HELP_ENGAGEMENT)
    
    improvement_areas = st.multiselect(FEEDBACK_LABEL_IMPROVEMENT_AREAS, 
        FEEDBACK_IMPROVEMENT_OPTIONS,
        help=FEEDBACK_HELP_IMPROVEMENT_AREAS)
    
    feedback = st.text_area(FEEDBACK_LABEL_OPEN_FEEDBACK, help=FEEDBACK_HELP_OPEN_FEEDBACK)
    
    future_plans = st.selectbox(FEEDBACK_LABEL_FUTURE_PLANS, FEEDBACK_FUTURE_PLANS_OPTIONS, help=FEEDBACK_HELP_FUTURE_PLANS)

    with st.expander(FEEDBACK_LABEL_ADDITIONAL_COMMENTS):
        strengths = st.text_area(FEEDBACK_LABEL_STRENGTHS, help=FEEDBACK_HELP_STRENGTHS)
        weaknesses = st.text_area(FEEDBACK_LABEL_WEAKNESSES, help=FEEDBACK_HELP_WEAKNESSES)

    submitted = st.form_submit_button(FEEDBACK_BUTTON_SUBMIT)

if submitted:
    if not program_name:
        st.error(FEEDBACK_ERROR_PROGRAM_NAME)
    elif not feedback:
        st.error(FEEDBACK_ERROR_FEEDBACK_REQUIRED)
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
            # Show progress bar if enabled
            if ENABLE_PROGRESS_BAR:
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
            st.success(FEEDBACK_SUCCESS_SUBMITTED)
            if ENABLE_BALLOONS:
                st.balloons()
        except Exception as e:
            st.error(FEEDBACK_ERROR_SAVE_FAILED.format(error=str(e)))

# Sidebar
st.sidebar.title(FEEDBACK_SIDEBAR_FAQ_TITLE)
faq_expander = st.sidebar.expander(FEEDBACK_SIDEBAR_FAQ_QUESTION)
with faq_expander:
    st.write(FEEDBACK_SIDEBAR_FAQ_ANSWER)

st.sidebar.info(FEEDBACK_SIDEBAR_INFO)

# Data privacy notice
st.sidebar.markdown("---")
st.sidebar.subheader(FEEDBACK_SIDEBAR_PRIVACY_TITLE)
st.sidebar.write(FEEDBACK_SIDEBAR_PRIVACY_TEXT)

# Footer
st.markdown("---")
st.markdown(FEEDBACK_FOOTER_COPYRIGHT)
