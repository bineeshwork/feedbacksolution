# =============================================================================
# Constants Module
# All static text strings extracted from app files for centralized management.
# =============================================================================

# =============================================================================
# SCHEDULING POLL APP (app.py) CONSTANTS
# =============================================================================

# Page Configuration
SCHEDULING_POLL_PAGE_TITLE = "Arkansas Scheduling Poll"

# CSS Styles
SCHEDULING_POLL_CSS = """
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
"""

# Date Options
SCHEDULING_POLL_DATE_OPTIONS = [
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
    "Monday, Oct 13", "Tuesday, Oct 14", "Wednesday, Oct 15", "Thursday, Oct 16", "Friday, Oct 17",
]

# S3 Configuration
SCHEDULING_POLL_S3_BUCKET_NAME = "awsbin-arkansasonline-poll"

# Header / Title
SCHEDULING_POLL_TITLE = "\U0001f4cd Arkansas Onsite Scheduling Poll"
SCHEDULING_POLL_INSTRUCTIONS = "Select **any dates** below you are **not available** to travel or attend the in-person event in **Little Rock, AR**."

# Form Labels
SCHEDULING_POLL_FORM_KEY = "availability_form"
SCHEDULING_POLL_NAME_LABEL = "Full Name"
SCHEDULING_POLL_EMAIL_LABEL = "Email Address"
SCHEDULING_POLL_DATES_LABEL = "What dates are you *NOT* available?"
SCHEDULING_POLL_COMMENTS_LABEL = "Optional Comments / Notes"
SCHEDULING_POLL_SUBMIT_LABEL = "Submit Availability"

# Messages
SCHEDULING_POLL_ERROR_NAME_EMAIL = "Please provide both your name and email."
SCHEDULING_POLL_WARNING_NO_DATES = "You haven't selected any dates. Are you available all dates?"
SCHEDULING_POLL_SUBMIT_SPINNER = "Submitting your response..."
SCHEDULING_POLL_SUCCESS_MESSAGE = "\u2705 Your availability has been submitted!"
SCHEDULING_POLL_ERROR_S3_INIT = "Failed to initialize AWS S3: {error}"
SCHEDULING_POLL_ERROR_SUBMIT = "\u274c Submission failed: {error}"

# Sidebar
SCHEDULING_POLL_SIDEBAR_TITLE = "\u2139\ufe0f About this Poll"
SCHEDULING_POLL_SIDEBAR_DESCRIPTION = """
This poll helps us schedule an in-person event based on staff availability.
Please select any dates you are **not available**.
"""
SCHEDULING_POLL_SIDEBAR_PRIVACY_TITLE = "\U0001f512 Data Privacy Notice"
SCHEDULING_POLL_SIDEBAR_PRIVACY_TEXT = """
Your responses are confidential and will only be used for internal scheduling purposes.
"""

# Footer
SCHEDULING_POLL_FOOTER = "\u00a9 2025 State of Arkansas Event Coordination Team"

# =============================================================================
# STUDENT FEEDBACK APP (studentfeedback_app.py) CONSTANTS
# =============================================================================

# Page Configuration
FEEDBACK_PAGE_TITLE = "Texas A&M Student Feedback Form"

# CSS Styles
FEEDBACK_CSS = """
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
"""

# S3 Configuration
FEEDBACK_S3_BUCKET_NAME = "awsbin-amazonq-assets"

# Header
FEEDBACK_IMAGE_PATH = "./primaryTAM.png"
FEEDBACK_TITLE = "Student Feedback Form"
FEEDBACK_SUBTITLE = "Your opinion matters! Help us improve our programs."

# Form Labels
FEEDBACK_FORM_KEY = "feedback_form"
FEEDBACK_PROGRAM_NAME_LABEL = "Program Name"
FEEDBACK_PROGRAM_NAME_HELP = "Enter the full name of your academic program"
FEEDBACK_COURSE_SATISFACTION_LABEL = "Course Satisfaction"
FEEDBACK_COURSE_SATISFACTION_HELP = "Rate your overall satisfaction with the course"
FEEDBACK_COURSE_SATISFACTION_SCALE = "1: Very Dissatisfied, 5: Very Satisfied"
FEEDBACK_LEARNING_OUTCOMES_LABEL = "Learning Outcomes Achievement"
FEEDBACK_LEARNING_OUTCOMES_HELP = "How well did the course meet its stated learning objectives?"
FEEDBACK_SUPPORT_SERVICES_LABEL = "Support Services Rating"
FEEDBACK_SUPPORT_SERVICES_HELP = "Rate the quality of support services provided"
FEEDBACK_ENGAGEMENT_LABEL = "Engagement Level"
FEEDBACK_ENGAGEMENT_OPTIONS = ["Low", "Medium", "High"]
FEEDBACK_ENGAGEMENT_DEFAULT = "Medium"
FEEDBACK_ENGAGEMENT_HELP = "How engaged were you in the course activities?"
FEEDBACK_IMPROVEMENT_AREAS_LABEL = "Areas for Improvement"
FEEDBACK_IMPROVEMENT_AREAS_OPTIONS = [
    "Course Content", "Teaching Methods", "Assessment", "Resources", "Support Services"
]
FEEDBACK_IMPROVEMENT_AREAS_HELP = "Select all areas where you think improvements can be made"
FEEDBACK_OPEN_ENDED_LABEL = "Open-ended Feedback"
FEEDBACK_OPEN_ENDED_HELP = "Please provide any additional comments or suggestions"
FEEDBACK_FUTURE_PLANS_LABEL = "Future Plans"
FEEDBACK_FUTURE_PLANS_OPTIONS = ["Continue", "Transfer", "Undecided"]
FEEDBACK_FUTURE_PLANS_HELP = "What are your plans for the next academic term?"
FEEDBACK_ADDITIONAL_COMMENTS_LABEL = "Additional Comments"
FEEDBACK_STRENGTHS_LABEL = "Program Strengths"
FEEDBACK_STRENGTHS_HELP = "What aspects of the program do you find most valuable?"
FEEDBACK_WEAKNESSES_LABEL = "Areas for Enhancement"
FEEDBACK_WEAKNESSES_HELP = "What aspects of the program could be improved?"
FEEDBACK_SUBMIT_LABEL = "Submit Feedback"

# Messages
FEEDBACK_ERROR_NO_PROGRAM = "Please enter your program name."
FEEDBACK_ERROR_NO_FEEDBACK = "Please provide some feedback in the open-ended section."
FEEDBACK_SUCCESS_MESSAGE = "Thank you! Your feedback has been submitted successfully."
FEEDBACK_ERROR_SAVE = "An error occurred while saving your feedback: {error}"

# Sidebar
FEEDBACK_SIDEBAR_TITLE = "Frequently Asked Questions"
FEEDBACK_FAQ_QUESTION = "Why is this feedback important?"
FEEDBACK_FAQ_ANSWER = "Your feedback helps us continuously improve our programs and enhance the learning experience for all Aggies."
FEEDBACK_SIDEBAR_INFO = "Your responses are anonymous and will be used solely for program improvement purposes."
FEEDBACK_SIDEBAR_PRIVACY_TITLE = "Data Privacy Notice"
FEEDBACK_SIDEBAR_PRIVACY_TEXT = """
We value your privacy. All responses are anonymized and securely stored. 
The data collected will only be used for program improvement purposes and will not be shared with third parties.
"""

# Footer
FEEDBACK_FOOTER = "\u00a9 2025 Texas A&M University. All rights reserved."

# =============================================================================
# LLM CONFIGURATION (utils/llm.py) CONSTANTS
# =============================================================================

LLM_MODEL_ID = "anthropic.claude-v2"
LLM_MAX_TOKENS = 4096
LLM_TEMPERATURE = 0.
LLM_ACCEPT_TYPE = "application/json"
LLM_CONTENT_TYPE = "application/json"
