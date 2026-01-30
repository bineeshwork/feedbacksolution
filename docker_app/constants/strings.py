"""
Centralized string constants for all UI text in the feedbacksolution application.
This module provides a single source of truth for all static text displayed to users.
"""

# =============================================================================
# ARKANSAS SCHEDULING POLL (app.py) STRINGS
# =============================================================================

# Page Configuration
APP_PAGE_TITLE = "Arkansas Scheduling Poll"

# Page Header
APP_MAIN_TITLE = "📍 Arkansas Onsite Scheduling Poll"
APP_INSTRUCTIONS = "Select **any dates** below you are **not available** to travel or attend the in-person event in **Little Rock, AR**."

# Form Labels
APP_LABEL_FULL_NAME = "Full Name"
APP_LABEL_EMAIL = "Email Address"
APP_LABEL_UNAVAILABLE_DATES = "What dates are you *NOT* available?"
APP_LABEL_COMMENTS = "Optional Comments / Notes"
APP_BUTTON_SUBMIT = "Submit Availability"

# Messages
APP_ERROR_NAME_EMAIL_REQUIRED = "Please provide both your name and email."
APP_WARNING_NO_DATES = "You haven't selected any dates. Are you available all dates?"
APP_SUCCESS_SUBMITTED = "✅ Your availability has been submitted!"
APP_SPINNER_SUBMITTING = "Submitting your response..."

# Error message templates (use .format() with these)
APP_ERROR_S3_INIT = "Failed to initialize AWS S3: {error}"
APP_ERROR_SUBMISSION_FAILED = "❌ Submission failed: {error}"

# Sidebar
APP_SIDEBAR_TITLE = "ℹ️ About this Poll"
APP_SIDEBAR_ABOUT = """
This poll helps us schedule an in-person event based on staff availability.
Please select any dates you are **not available**.
"""
APP_SIDEBAR_PRIVACY_TITLE = "🔒 Data Privacy Notice"
APP_SIDEBAR_PRIVACY_TEXT = """
Your responses are confidential and will only be used for internal scheduling purposes.
"""

# Footer
APP_FOOTER_COPYRIGHT = "© 2025 State of Arkansas Event Coordination Team"


# =============================================================================
# STUDENT FEEDBACK FORM (studentfeedback_app.py) STRINGS
# =============================================================================

# Page Configuration
FEEDBACK_PAGE_TITLE = "Texas A&M Student Feedback Form"

# Page Header
FEEDBACK_MAIN_TITLE = "Student Feedback Form"
FEEDBACK_DESCRIPTION = "Your opinion matters! Help us improve our programs."

# Anonymized ID (use .format() with student_id)
FEEDBACK_ANONYMIZED_ID = "Your anonymized Student ID: {student_id}"

# Form Labels
FEEDBACK_LABEL_PROGRAM_NAME = "Program Name"
FEEDBACK_HELP_PROGRAM_NAME = "Enter the full name of your academic program"

FEEDBACK_LABEL_COURSE_SATISFACTION = "Course Satisfaction"
FEEDBACK_HELP_COURSE_SATISFACTION = "Rate your overall satisfaction with the course"
FEEDBACK_SLIDER_SATISFACTION_DESCRIPTION = "1: Very Dissatisfied, 5: Very Satisfied"

FEEDBACK_LABEL_LEARNING_OUTCOMES = "Learning Outcomes Achievement"
FEEDBACK_HELP_LEARNING_OUTCOMES = "How well did the course meet its stated learning objectives?"

FEEDBACK_LABEL_SUPPORT_SERVICES = "Support Services Rating"
FEEDBACK_HELP_SUPPORT_SERVICES = "Rate the quality of support services provided"

FEEDBACK_LABEL_ENGAGEMENT = "Engagement Level"
FEEDBACK_HELP_ENGAGEMENT = "How engaged were you in the course activities?"
FEEDBACK_ENGAGEMENT_OPTIONS = ["Low", "Medium", "High"]
FEEDBACK_ENGAGEMENT_DEFAULT = "Medium"

FEEDBACK_LABEL_IMPROVEMENT_AREAS = "Areas for Improvement"
FEEDBACK_HELP_IMPROVEMENT_AREAS = "Select all areas where you think improvements can be made"
FEEDBACK_IMPROVEMENT_OPTIONS = [
    "Course Content",
    "Teaching Methods",
    "Assessment",
    "Resources",
    "Support Services"
]

FEEDBACK_LABEL_OPEN_FEEDBACK = "Open-ended Feedback"
FEEDBACK_HELP_OPEN_FEEDBACK = "Please provide any additional comments or suggestions"

FEEDBACK_LABEL_FUTURE_PLANS = "Future Plans"
FEEDBACK_HELP_FUTURE_PLANS = "What are your plans for the next academic term?"
FEEDBACK_FUTURE_PLANS_OPTIONS = ["Continue", "Transfer", "Undecided"]

FEEDBACK_LABEL_ADDITIONAL_COMMENTS = "Additional Comments"
FEEDBACK_LABEL_STRENGTHS = "Program Strengths"
FEEDBACK_HELP_STRENGTHS = "What aspects of the program do you find most valuable?"
FEEDBACK_LABEL_WEAKNESSES = "Areas for Enhancement"
FEEDBACK_HELP_WEAKNESSES = "What aspects of the program could be improved?"

# Form Button
FEEDBACK_BUTTON_SUBMIT = "Submit Feedback"

# Validation Messages
FEEDBACK_ERROR_PROGRAM_NAME = "Please enter your program name."
FEEDBACK_ERROR_FEEDBACK_REQUIRED = "Please provide some feedback in the open-ended section."

# Success/Error Messages (use .format() for error template)
FEEDBACK_SUCCESS_SUBMITTED = "Thank you! Your feedback has been submitted successfully."
FEEDBACK_ERROR_SAVE_FAILED = "An error occurred while saving your feedback: {error}"

# Sidebar
FEEDBACK_SIDEBAR_FAQ_TITLE = "Frequently Asked Questions"
FEEDBACK_SIDEBAR_FAQ_QUESTION = "Why is this feedback important?"
FEEDBACK_SIDEBAR_FAQ_ANSWER = "Your feedback helps us continuously improve our programs and enhance the learning experience for all Aggies."
FEEDBACK_SIDEBAR_INFO = "Your responses are anonymous and will be used solely for program improvement purposes."
FEEDBACK_SIDEBAR_PRIVACY_TITLE = "Data Privacy Notice"
FEEDBACK_SIDEBAR_PRIVACY_TEXT = """
We value your privacy. All responses are anonymized and securely stored. 
The data collected will only be used for program improvement purposes and will not be shared with third parties.
"""

# Footer
FEEDBACK_FOOTER_COPYRIGHT = "© 2025 Texas A&M University. All rights reserved."
