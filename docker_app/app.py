import streamlit as st
import json
import boto3
import uuid
import time
import os
from datetime import datetime

from constants import (
    SCHEDULING_POLL_PAGE_TITLE,
    SCHEDULING_POLL_CSS,
    SCHEDULING_POLL_DATE_OPTIONS,
    SCHEDULING_POLL_S3_BUCKET_NAME,
    SCHEDULING_POLL_TITLE,
    SCHEDULING_POLL_INSTRUCTIONS,
    SCHEDULING_POLL_FORM_KEY,
    SCHEDULING_POLL_NAME_LABEL,
    SCHEDULING_POLL_EMAIL_LABEL,
    SCHEDULING_POLL_DATES_LABEL,
    SCHEDULING_POLL_COMMENTS_LABEL,
    SCHEDULING_POLL_SUBMIT_LABEL,
    SCHEDULING_POLL_ERROR_NAME_EMAIL,
    SCHEDULING_POLL_WARNING_NO_DATES,
    SCHEDULING_POLL_SUBMIT_SPINNER,
    SCHEDULING_POLL_SUCCESS_MESSAGE,
    SCHEDULING_POLL_ERROR_S3_INIT,
    SCHEDULING_POLL_ERROR_SUBMIT,
    SCHEDULING_POLL_SIDEBAR_TITLE,
    SCHEDULING_POLL_SIDEBAR_DESCRIPTION,
    SCHEDULING_POLL_SIDEBAR_PRIVACY_TITLE,
    SCHEDULING_POLL_SIDEBAR_PRIVACY_TEXT,
    SCHEDULING_POLL_FOOTER,
)

# Set Streamlit page configuration
st.set_page_config(page_title=SCHEDULING_POLL_PAGE_TITLE, layout="centered")

# Custom styling using markdown
st.markdown(SCHEDULING_POLL_CSS, unsafe_allow_html=True)

# AWS S3 Configuration
USE_S3 = True  # Set to False to disable S3 and save locally
S3_BUCKET_NAME = SCHEDULING_POLL_S3_BUCKET_NAME

# Initialize S3 Client if needed
if USE_S3:
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        )
    except Exception as e:
        st.error(SCHEDULING_POLL_ERROR_S3_INIT.format(error=str(e)))
        st.stop()

# Header Section
st.title(SCHEDULING_POLL_TITLE)
st.write(SCHEDULING_POLL_INSTRUCTIONS)

# Main Form
with st.form(SCHEDULING_POLL_FORM_KEY):
    respondent_id = str(uuid.uuid4())[:8]
    name = st.text_input(SCHEDULING_POLL_NAME_LABEL)
    email = st.text_input(SCHEDULING_POLL_EMAIL_LABEL)
    unavailable_dates = st.multiselect(SCHEDULING_POLL_DATES_LABEL, SCHEDULING_POLL_DATE_OPTIONS)

    comments = st.text_area(SCHEDULING_POLL_COMMENTS_LABEL)

    submit = st.form_submit_button(SCHEDULING_POLL_SUBMIT_LABEL)

# Handle submission
if submit:
    if not name or not email:
        st.error(SCHEDULING_POLL_ERROR_NAME_EMAIL)
    elif not unavailable_dates:
        st.warning(SCHEDULING_POLL_WARNING_NO_DATES)
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
            with st.spinner(SCHEDULING_POLL_SUBMIT_SPINNER):
                filename = f"arkansas_poll_{respondent_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

                if USE_S3:
                    s3.put_object(
                        Bucket=S3_BUCKET_NAME,
                        Key=f"scheduling/{filename}",
                        Body=json_data
                    )
                else:
                    # Save locally
                    with open(f"./{filename}", "w") as file:
                        file.write(json_data)

                st.success(SCHEDULING_POLL_SUCCESS_MESSAGE)
                st.balloons()
        except Exception as e:
            st.error(SCHEDULING_POLL_ERROR_SUBMIT.format(error=e))

# Sidebar Helper
st.sidebar.title(SCHEDULING_POLL_SIDEBAR_TITLE)
st.sidebar.write(SCHEDULING_POLL_SIDEBAR_DESCRIPTION)
st.sidebar.markdown("---")
st.sidebar.subheader(SCHEDULING_POLL_SIDEBAR_PRIVACY_TITLE)
st.sidebar.write(SCHEDULING_POLL_SIDEBAR_PRIVACY_TEXT)

# Footer
st.markdown("---")
st.caption(SCHEDULING_POLL_FOOTER)
