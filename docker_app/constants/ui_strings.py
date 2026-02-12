"""
Centralized UI text strings for all Streamlit applications.
This module contains all static text used in the user interface.
"""

# ==============================================================================
# ARKANSAS SCHEDULING POLL (app.py)
# ==============================================================================

# Page Configuration
ARKANSAS_PAGE_TITLE = "Arkansas Scheduling Poll"

# Page Header
ARKANSAS_TITLE = "📍 Arkansas Onsite Scheduling Poll"
ARKANSAS_INSTRUCTION_TEXT = "Select **any dates** below you are **not available** to travel or attend the in-person event in **Little Rock, AR**."

# Form Labels
ARKANSAS_LABEL_FULL_NAME = "Full Name"
ARKANSAS_LABEL_EMAIL = "Email Address"
ARKANSAS_LABEL_UNAVAILABLE_DATES = "What dates are you *NOT* available?"
ARKANSAS_LABEL_COMMENTS = "Optional Comments / Notes"
ARKANSAS_BUTTON_SUBMIT = "Submit Availability"

# Messages
ARKANSAS_ERROR_NAME_EMAIL_REQUIRED = "Please provide both your name and email."
ARKANSAS_WARNING_NO_DATES_SELECTED = "You haven't selected any dates. Are you available all dates?"
ARKANSAS_SPINNER_SUBMITTING = "Submitting your response..."
ARKANSAS_SUCCESS_SUBMITTED = "✅ Your availability has been submitted!"
ARKANSAS_ERROR_SUBMISSION_FAILED = "❌ Submission failed: {error}"
ARKANSAS_ERROR_S3_INIT_FAILED = "Failed to initialize AWS S3: {error}"

# Sidebar Content
ARKANSAS_SIDEBAR_TITLE = "ℹ️ About this Poll"
ARKANSAS_SIDEBAR_DESCRIPTION = """
This poll helps us schedule an in-person event based on staff availability.
Please select any dates you are **not available**.
"""
ARKANSAS_SIDEBAR_PRIVACY_TITLE = "🔒 Data Privacy Notice"
ARKANSAS_SIDEBAR_PRIVACY_TEXT = """
Your responses are confidential and will only be used for internal scheduling purposes.
"""

# Footer
ARKANSAS_FOOTER_TEXT = "© 2025 State of Arkansas Event Coordination Team"


# ==============================================================================
# STUDENT FEEDBACK FORM (studentfeedback_app.py)
# ==============================================================================

# Page Configuration
STUDENT_PAGE_TITLE = "Texas A&M Student Feedback Form"

# Page Header
STUDENT_TITLE = "Student Feedback Form"
STUDENT_DESCRIPTION = "Your opinion matters! Help us improve our programs."
STUDENT_ID_TEXT = "Your anonymized Student ID: {student_id}"

# Form Labels
STUDENT_LABEL_PROGRAM_NAME = "Program Name"
STUDENT_HELP_PROGRAM_NAME = "Enter the full name of your academic program"

STUDENT_LABEL_COURSE_SATISFACTION = "Course Satisfaction"
STUDENT_HELP_COURSE_SATISFACTION = "Rate your overall satisfaction with the course"
STUDENT_SATISFACTION_SCALE_TEXT = "1: Very Dissatisfied, 5: Very Satisfied"

STUDENT_LABEL_LEARNING_OUTCOMES = "Learning Outcomes Achievement"
STUDENT_HELP_LEARNING_OUTCOMES = "How well did the course meet its stated learning objectives?"

STUDENT_LABEL_SUPPORT_SERVICES = "Support Services Rating"
STUDENT_HELP_SUPPORT_SERVICES = "Rate the quality of support services provided"

STUDENT_LABEL_ENGAGEMENT_LEVEL = "Engagement Level"
STUDENT_HELP_ENGAGEMENT_LEVEL = "How engaged were you in the course activities?"
STUDENT_ENGAGEMENT_OPTIONS = ["Low", "Medium", "High"]
STUDENT_ENGAGEMENT_DEFAULT = "Medium"

STUDENT_LABEL_IMPROVEMENT_AREAS = "Areas for Improvement"
STUDENT_HELP_IMPROVEMENT_AREAS = "Select all areas where you think improvements can be made"
STUDENT_IMPROVEMENT_AREA_OPTIONS = [
    "Course Content",
    "Teaching Methods",
    "Assessment",
    "Resources",
    "Support Services"
]

STUDENT_LABEL_OPEN_FEEDBACK = "Open-ended Feedback"
STUDENT_HELP_OPEN_FEEDBACK = "Please provide any additional comments or suggestions"

STUDENT_LABEL_FUTURE_PLANS = "Future Plans"
STUDENT_HELP_FUTURE_PLANS = "What are your plans for the next academic term?"
STUDENT_FUTURE_PLANS_OPTIONS = ["Continue", "Transfer", "Undecided"]

STUDENT_EXPANDER_ADDITIONAL_COMMENTS = "Additional Comments"
STUDENT_LABEL_STRENGTHS = "Program Strengths"
STUDENT_HELP_STRENGTHS = "What aspects of the program do you find most valuable?"
STUDENT_LABEL_WEAKNESSES = "Areas for Enhancement"
STUDENT_HELP_WEAKNESSES = "What aspects of the program could be improved?"

STUDENT_BUTTON_SUBMIT = "Submit Feedback"

# Messages
STUDENT_ERROR_PROGRAM_NAME_REQUIRED = "Please enter your program name."
STUDENT_ERROR_FEEDBACK_REQUIRED = "Please provide some feedback in the open-ended section."
STUDENT_SUCCESS_SUBMITTED = "Thank you! Your feedback has been submitted successfully."
STUDENT_ERROR_SAVE_FAILED = "An error occurred while saving your feedback: {error}"

# Sidebar Content
STUDENT_SIDEBAR_TITLE = "Frequently Asked Questions"
STUDENT_FAQ_EXPANDER_TITLE = "Why is this feedback important?"
STUDENT_FAQ_ANSWER = "Your feedback helps us continuously improve our programs and enhance the learning experience for all Aggies."
STUDENT_SIDEBAR_INFO = "Your responses are anonymous and will be used solely for program improvement purposes."
STUDENT_SIDEBAR_PRIVACY_TITLE = "Data Privacy Notice"
STUDENT_SIDEBAR_PRIVACY_TEXT = """
We value your privacy. All responses are anonymized and securely stored. 
The data collected will only be used for program improvement purposes and will not be shared with third parties.
"""

# Footer
STUDENT_FOOTER_TEXT = "© 2025 Texas A&M University. All rights reserved."
