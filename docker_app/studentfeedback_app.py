import streamlit as st
import boto3
import json
import uuid
from datetime import datetime
import time
import os

from strings import (
    STUDENT_FEEDBACK_PAGE_TITLE,
    STUDENT_FEEDBACK_TITLE,
    STUDENT_FEEDBACK_SUBTITLE,
    STUDENT_ID_FORMAT,
    LABEL_PROGRAM_NAME,
    LABEL_COURSE_SATISFACTION,
    LABEL_LEARNING_OUTCOMES,
    LABEL_SUPPORT_SERVICES,
    LABEL_ENGAGEMENT_LEVEL,
    LABEL_AREAS_FOR_IMPROVEMENT,
    LABEL_OPEN_FEEDBACK,
    LABEL_FUTURE_PLANS,
    LABEL_PROGRAM_STRENGTHS,
    LABEL_AREAS_ENHANCEMENT,
    LABEL_ADDITIONAL_COMMENTS,
    LABEL_SUBMIT_FEEDBACK,
    HELP_PROGRAM_NAME,
    HELP_COURSE_SATISFACTION,
    HELP_LEARNING_OUTCOMES,
    HELP_SUPPORT_SERVICES,
    HELP_ENGAGEMENT_LEVEL,
    HELP_AREAS_FOR_IMPROVEMENT,
    HELP_OPEN_FEEDBACK,
    HELP_FUTURE_PLANS,
    HELP_PROGRAM_STRENGTHS,
    HELP_AREAS_ENHANCEMENT,
    SLIDER_SCALE_DESCRIPTION,
    ENGAGEMENT_OPTIONS,
    ENGAGEMENT_DEFAULT,
    IMPROVEMENT_AREAS_OPTIONS,
    FUTURE_PLANS_OPTIONS,
    SUCCESS_FEEDBACK_SUBMITTED,
    ERROR_PROGRAM_NAME_REQUIRED,
    ERROR_FEEDBACK_REQUIRED,
    ERROR_SAVE_FEEDBACK,
    SIDEBAR_TITLE_FAQ,
    SIDEBAR_FAQ_QUESTION,
    SIDEBAR_FAQ_ANSWER,
    SIDEBAR_ANONYMOUS_INFO,
    SIDEBAR_PRIVACY_TITLE,
    SIDEBAR_PRIVACY_TEXT,
    FOOTER_TEXT,
)

# Set page config
st.set_page_config(page_title=STUDENT_FEEDBACK_PAGE_TITLE, layout="wide")

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
st.title(STUDENT_FEEDBACK_TITLE)
st.write(STUDENT_FEEDBACK_SUBTITLE)

# Main form
with st.form("feedback_form"):
    student_id = str(uuid.uuid4())[:8]  # Generate anonymized ID
    st.write(STUDENT_ID_FORMAT.format(student_id=student_id))

    program_name = st.text_input(LABEL_PROGRAM_NAME, help=HELP_PROGRAM_NAME)
    
    course_satisfaction = st.slider(LABEL_COURSE_SATISFACTION, 1, 5, 3, help=HELP_COURSE_SATISFACTION)
    st.write(SLIDER_SCALE_DESCRIPTION)
    
    learning_outcomes = st.slider(LABEL_LEARNING_OUTCOMES, 1, 5, 3, help=HELP_LEARNING_OUTCOMES)
    
    support_services = st.slider(LABEL_SUPPORT_SERVICES, 1, 5, 3, help=HELP_SUPPORT_SERVICES)
    
    engagement_level = st.select_slider(LABEL_ENGAGEMENT_LEVEL, options=ENGAGEMENT_OPTIONS, value=ENGAGEMENT_DEFAULT, help=HELP_ENGAGEMENT_LEVEL)
    
    improvement_areas = st.multiselect(LABEL_AREAS_FOR_IMPROVEMENT, 
        IMPROVEMENT_AREAS_OPTIONS,
        help=HELP_AREAS_FOR_IMPROVEMENT)
    
    feedback = st.text_area(LABEL_OPEN_FEEDBACK, help=HELP_OPEN_FEEDBACK)
    
    future_plans = st.selectbox(LABEL_FUTURE_PLANS, FUTURE_PLANS_OPTIONS, help=HELP_FUTURE_PLANS)

    with st.expander(LABEL_ADDITIONAL_COMMENTS):
        strengths = st.text_area(LABEL_PROGRAM_STRENGTHS, help=HELP_PROGRAM_STRENGTHS)
        weaknesses = st.text_area(LABEL_AREAS_ENHANCEMENT, help=HELP_AREAS_ENHANCEMENT)

    submitted = st.form_submit_button(LABEL_SUBMIT_FEEDBACK)

if submitted:
    if not program_name:
        st.error(ERROR_PROGRAM_NAME_REQUIRED)
    elif not feedback:
        st.error(ERROR_FEEDBACK_REQUIRED)
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
            st.success(SUCCESS_FEEDBACK_SUBMITTED)
            st.balloons()
        except Exception as e:
            st.error(ERROR_SAVE_FEEDBACK.format(error=str(e)))

# Sidebar
st.sidebar.title(SIDEBAR_TITLE_FAQ)
faq_expander = st.sidebar.expander(SIDEBAR_FAQ_QUESTION)
with faq_expander:
    st.write(SIDEBAR_FAQ_ANSWER)

st.sidebar.info(SIDEBAR_ANONYMOUS_INFO)

# Data privacy notice
st.sidebar.markdown("---")
st.sidebar.subheader(SIDEBAR_PRIVACY_TITLE)
st.sidebar.write(SIDEBAR_PRIVACY_TEXT)

# Footer
st.markdown("---")
st.markdown(FOOTER_TEXT)
