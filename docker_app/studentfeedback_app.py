import streamlit as st
import boto3
import json
import uuid
from datetime import datetime
import time
import os

from constants import (
    FEEDBACK_PAGE_TITLE,
    FEEDBACK_CSS,
    FEEDBACK_S3_BUCKET_NAME,
    FEEDBACK_IMAGE_PATH,
    FEEDBACK_TITLE,
    FEEDBACK_SUBTITLE,
    FEEDBACK_FORM_KEY,
    FEEDBACK_PROGRAM_NAME_LABEL,
    FEEDBACK_PROGRAM_NAME_HELP,
    FEEDBACK_COURSE_SATISFACTION_LABEL,
    FEEDBACK_COURSE_SATISFACTION_HELP,
    FEEDBACK_COURSE_SATISFACTION_SCALE,
    FEEDBACK_LEARNING_OUTCOMES_LABEL,
    FEEDBACK_LEARNING_OUTCOMES_HELP,
    FEEDBACK_SUPPORT_SERVICES_LABEL,
    FEEDBACK_SUPPORT_SERVICES_HELP,
    FEEDBACK_ENGAGEMENT_LABEL,
    FEEDBACK_ENGAGEMENT_OPTIONS,
    FEEDBACK_ENGAGEMENT_DEFAULT,
    FEEDBACK_ENGAGEMENT_HELP,
    FEEDBACK_IMPROVEMENT_AREAS_LABEL,
    FEEDBACK_IMPROVEMENT_AREAS_OPTIONS,
    FEEDBACK_IMPROVEMENT_AREAS_HELP,
    FEEDBACK_OPEN_ENDED_LABEL,
    FEEDBACK_OPEN_ENDED_HELP,
    FEEDBACK_FUTURE_PLANS_LABEL,
    FEEDBACK_FUTURE_PLANS_OPTIONS,
    FEEDBACK_FUTURE_PLANS_HELP,
    FEEDBACK_ADDITIONAL_COMMENTS_LABEL,
    FEEDBACK_STRENGTHS_LABEL,
    FEEDBACK_STRENGTHS_HELP,
    FEEDBACK_WEAKNESSES_LABEL,
    FEEDBACK_WEAKNESSES_HELP,
    FEEDBACK_SUBMIT_LABEL,
    FEEDBACK_ERROR_NO_PROGRAM,
    FEEDBACK_ERROR_NO_FEEDBACK,
    FEEDBACK_SUCCESS_MESSAGE,
    FEEDBACK_ERROR_SAVE,
    FEEDBACK_SIDEBAR_TITLE,
    FEEDBACK_FAQ_QUESTION,
    FEEDBACK_FAQ_ANSWER,
    FEEDBACK_SIDEBAR_INFO,
    FEEDBACK_SIDEBAR_PRIVACY_TITLE,
    FEEDBACK_SIDEBAR_PRIVACY_TEXT,
    FEEDBACK_FOOTER,
)

# Set page config
st.set_page_config(page_title=FEEDBACK_PAGE_TITLE, layout="wide")

# Custom theme for Texas A&M
st.markdown(FEEDBACK_CSS, unsafe_allow_html=True)

# Set up S3 client using environment variables
s3 = boto3.client('s3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_DEFAULT_REGION')
)

# Get S3 bucket name from environment variable
S3_BUCKET_NAME = FEEDBACK_S3_BUCKET_NAME

# Header
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(FEEDBACK_IMAGE_PATH, width=300)
st.title(FEEDBACK_TITLE)
st.write(FEEDBACK_SUBTITLE)

# Main form
with st.form(FEEDBACK_FORM_KEY):
    student_id = str(uuid.uuid4())[:8]  # Generate anonymized ID
    st.write(f"Your anonymized Student ID: {student_id}")

    program_name = st.text_input(FEEDBACK_PROGRAM_NAME_LABEL, help=FEEDBACK_PROGRAM_NAME_HELP)
    
    course_satisfaction = st.slider(FEEDBACK_COURSE_SATISFACTION_LABEL, 1, 5, 3, help=FEEDBACK_COURSE_SATISFACTION_HELP)
    st.write(FEEDBACK_COURSE_SATISFACTION_SCALE)
    
    learning_outcomes = st.slider(FEEDBACK_LEARNING_OUTCOMES_LABEL, 1, 5, 3, help=FEEDBACK_LEARNING_OUTCOMES_HELP)
    
    support_services = st.slider(FEEDBACK_SUPPORT_SERVICES_LABEL, 1, 5, 3, help=FEEDBACK_SUPPORT_SERVICES_HELP)
    
    engagement_level = st.select_slider(FEEDBACK_ENGAGEMENT_LABEL, options=FEEDBACK_ENGAGEMENT_OPTIONS, value=FEEDBACK_ENGAGEMENT_DEFAULT, help=FEEDBACK_ENGAGEMENT_HELP)
    
    improvement_areas = st.multiselect(FEEDBACK_IMPROVEMENT_AREAS_LABEL, 
        FEEDBACK_IMPROVEMENT_AREAS_OPTIONS,
        help=FEEDBACK_IMPROVEMENT_AREAS_HELP)
    
    feedback = st.text_area(FEEDBACK_OPEN_ENDED_LABEL, help=FEEDBACK_OPEN_ENDED_HELP)
    
    future_plans = st.selectbox(FEEDBACK_FUTURE_PLANS_LABEL, FEEDBACK_FUTURE_PLANS_OPTIONS, help=FEEDBACK_FUTURE_PLANS_HELP)

    with st.expander(FEEDBACK_ADDITIONAL_COMMENTS_LABEL):
        strengths = st.text_area(FEEDBACK_STRENGTHS_LABEL, help=FEEDBACK_STRENGTHS_HELP)
        weaknesses = st.text_area(FEEDBACK_WEAKNESSES_LABEL, help=FEEDBACK_WEAKNESSES_HELP)

    submitted = st.form_submit_button(FEEDBACK_SUBMIT_LABEL)

if submitted:
    if not program_name:
        st.error(FEEDBACK_ERROR_NO_PROGRAM)
    elif not feedback:
        st.error(FEEDBACK_ERROR_NO_FEEDBACK)
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
            st.success(FEEDBACK_SUCCESS_MESSAGE)
            st.balloons()
        except Exception as e:
            st.error(FEEDBACK_ERROR_SAVE.format(error=str(e)))

# Sidebar
st.sidebar.title(FEEDBACK_SIDEBAR_TITLE)
faq_expander = st.sidebar.expander(FEEDBACK_FAQ_QUESTION)
with faq_expander:
    st.write(FEEDBACK_FAQ_ANSWER)

st.sidebar.info(FEEDBACK_SIDEBAR_INFO)

# Data privacy notice
st.sidebar.markdown("---")
st.sidebar.subheader(FEEDBACK_SIDEBAR_PRIVACY_TITLE)
st.sidebar.write(FEEDBACK_SIDEBAR_PRIVACY_TEXT)

# Footer
st.markdown("---")
st.markdown(FEEDBACK_FOOTER)
