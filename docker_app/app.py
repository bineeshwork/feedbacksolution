import streamlit as st
import json
import boto3
import uuid
import time
import os
from datetime import datetime

from constants.strings import (
    APP_PAGE_TITLE,
    APP_MAIN_TITLE,
    APP_INSTRUCTIONS,
    APP_LABEL_FULL_NAME,
    APP_LABEL_EMAIL,
    APP_LABEL_UNAVAILABLE_DATES,
    APP_LABEL_COMMENTS,
    APP_BUTTON_SUBMIT,
    APP_ERROR_NAME_EMAIL_REQUIRED,
    APP_WARNING_NO_DATES,
    APP_SUCCESS_SUBMITTED,
    APP_SPINNER_SUBMITTING,
    APP_ERROR_S3_INIT,
    APP_ERROR_SUBMISSION_FAILED,
    APP_SIDEBAR_TITLE,
    APP_SIDEBAR_ABOUT,
    APP_SIDEBAR_PRIVACY_TITLE,
    APP_SIDEBAR_PRIVACY_TEXT,
    APP_FOOTER_COPYRIGHT,
)
from constants.config import (
    APP_USE_S3,
    APP_S3_BUCKET_NAME,
    APP_S3_KEY_PREFIX,
    DEFAULT_AWS_REGION,
    ENABLE_BALLOONS,
)

# Set Streamlit page configuration
st.set_page_config(page_title=APP_PAGE_TITLE, layout="centered")

# Custom styling using markdown
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }
    h1, h2, h3 {
        font-family: 'Oswald', sans-serif;
        color: #500000;
    }
    .stButton > button {
        background-color: #500000;
        color: white;
        font-weight: bold;
    }
    .stTextInput > div > input {
        font-family: 'Open Sans', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 📅 DATE OPTIONS
date_options = [
    "Monday, Aug 4", "Tuesday, Aug 5", "Wednesday, Aug 6", "Thursday, Aug 7", "Friday, Aug 8",
    "Monday, Aug 11", "Tuesday, Aug 12", "Wednesday, Aug 13", "Thursday, Aug 14", "Friday, Aug 15",
    "Monday, Aug 18", "Tuesday, Aug 19", "Wednesday, Aug 20", "Thursday, Aug 21", "Friday, Aug 22",
    "Monday, Aug 25", "Tuesday, Aug 26", "Wednesday, Aug 27", "Thursday, Aug 28", "Friday, Aug 29",
    "Tuesday, Sep 2", "Wednesday, Sep 3", "Thursday, Sep 4", "Friday, Sep 5",
    "Monday, Sep 8", "Tuesday, Sep 9", "Wednesday, Sep 10", "Thursday, Sep 11", "Friday, Sep 12",
    "Monday, Sep 15", "Tuesday, Sep 16", "Wednesday, Sep 17", "Thursday, Sep 18", "Friday, Sep 19",
    "Monday, Sep 22", "Tuesday, Sep 23", "Wednesday, Sep 24", "Thursday, Sep 25", "Friday, Sep 26",
    "Monday, Sep 29", "Tuesday, Sep 30", "Wednesday, Oct 1", "Thursday, Oct 2", "Friday, Oct 3",
    "Monday, Oct 6", "Tuesday, Oct 7", "Wednesday, Oct 8", "Thursday, Oct 9", "Friday, Oct 10",
    "Monday, Oct 13", "Tuesday, Oct 14", "Wednesday, Oct 15", "Thursday, Oct 16", "Friday, Oct 17"
]

# AWS S3 Configuration (using environment variables from config)
USE_S3 = APP_USE_S3
S3_BUCKET_NAME = APP_S3_BUCKET_NAME

# Initialize S3 Client if needed
if USE_S3:
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', DEFAULT_AWS_REGION)
        )
    except Exception as e:
        st.error(APP_ERROR_S3_INIT.format(error=str(e)))
        st.stop()

# Header Section
st.title(APP_MAIN_TITLE)
st.write(APP_INSTRUCTIONS)

# Main Form
with st.form("availability_form"):
    respondent_id = str(uuid.uuid4())[:8]
    name = st.text_input(APP_LABEL_FULL_NAME)
    email = st.text_input(APP_LABEL_EMAIL)
    unavailable_dates = st.multiselect(APP_LABEL_UNAVAILABLE_DATES, date_options)

    comments = st.text_area(APP_LABEL_COMMENTS)

    submit = st.form_submit_button(APP_BUTTON_SUBMIT)

# Handle submission
if submit:
    if not name or not email:
        st.error(APP_ERROR_NAME_EMAIL_REQUIRED)
    elif not unavailable_dates:
        st.warning(APP_WARNING_NO_DATES)
    else:
        submission = {
            "Respondent ID": respondent_id,
            "Name": name,
            "Email": email,
            "Unavailable Dates": unavailable_dates,
            "Comments": comments,
            "Submitted At": datetime.now().isoformat()
        }

        # Convert to JSON string
        json_data = json.dumps(submission, indent=2)

        try:
            # Show progress bar
            with st.spinner(APP_SPINNER_SUBMITTING):
                filename = f"arkansas_poll_{respondent_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

                if USE_S3:
                    s3.put_object(
                        Bucket=S3_BUCKET_NAME,
                        Key=f"{APP_S3_KEY_PREFIX}/{filename}",
                        Body=json_data
                    )
                else:
                    # Save locally
                    with open(f"./{filename}", "w") as file:
                        file.write(json_data)

                st.success(APP_SUCCESS_SUBMITTED)
                if ENABLE_BALLOONS:
                    st.balloons()
        except Exception as e:
            st.error(APP_ERROR_SUBMISSION_FAILED.format(error=e))

# Sidebar Helper
st.sidebar.title(APP_SIDEBAR_TITLE)
st.sidebar.write(APP_SIDEBAR_ABOUT)
st.sidebar.markdown("---")
st.sidebar.subheader(APP_SIDEBAR_PRIVACY_TITLE)
st.sidebar.write(APP_SIDEBAR_PRIVACY_TEXT)

# Footer
st.markdown("---")
st.caption(APP_FOOTER_COPYRIGHT)
