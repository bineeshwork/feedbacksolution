"""
Centralized string constants for the feedback application.
This module contains all user-facing text strings used in the application.
"""

# =============================================================================
# STUDENT FEEDBACK APP STRINGS (studentfeedback_app.py)
# =============================================================================

# Page Configuration
STUDENT_FEEDBACK_PAGE_TITLE = "Texas A&M Student Feedback Form"

# Header Section
STUDENT_FEEDBACK_TITLE = "Student Feedback Form"
STUDENT_FEEDBACK_SUBTITLE = "Your opinion matters! Help us improve our programs."
STUDENT_ID_FORMAT = "Your anonymized Student ID: {student_id}"

# Form Labels
LABEL_PROGRAM_NAME = "Program Name"
LABEL_COURSE_SATISFACTION = "Course Satisfaction"
LABEL_LEARNING_OUTCOMES = "Learning Outcomes Achievement"
LABEL_SUPPORT_SERVICES = "Support Services Rating"
LABEL_ENGAGEMENT_LEVEL = "Engagement Level"
LABEL_AREAS_FOR_IMPROVEMENT = "Areas for Improvement"
LABEL_OPEN_FEEDBACK = "Open-ended Feedback"
LABEL_FUTURE_PLANS = "Future Plans"
LABEL_PROGRAM_STRENGTHS = "Program Strengths"
LABEL_AREAS_ENHANCEMENT = "Areas for Enhancement"
LABEL_ADDITIONAL_COMMENTS = "Additional Comments"
LABEL_SUBMIT_FEEDBACK = "Submit Feedback"

# Help Text Strings
HELP_PROGRAM_NAME = "Enter the full name of your academic program"
HELP_COURSE_SATISFACTION = "Rate your overall satisfaction with the course"
HELP_LEARNING_OUTCOMES = "How well did the course meet its stated learning objectives?"
HELP_SUPPORT_SERVICES = "Rate the quality of support services provided"
HELP_ENGAGEMENT_LEVEL = "How engaged were you in the course activities?"
HELP_AREAS_FOR_IMPROVEMENT = "Select all areas where you think improvements can be made"
HELP_OPEN_FEEDBACK = "Please provide any additional comments or suggestions"
HELP_FUTURE_PLANS = "What are your plans for the next academic term?"
HELP_PROGRAM_STRENGTHS = "What aspects of the program do you find most valuable?"
HELP_AREAS_ENHANCEMENT = "What aspects of the program could be improved?"

# Slider Scale Description
SLIDER_SCALE_DESCRIPTION = "1: Very Dissatisfied, 5: Very Satisfied"

# Dropdown/Select Options
ENGAGEMENT_OPTIONS = ["Low", "Medium", "High"]
ENGAGEMENT_DEFAULT = "Medium"
IMPROVEMENT_AREAS_OPTIONS = ["Course Content", "Teaching Methods", "Assessment", "Resources", "Support Services"]
FUTURE_PLANS_OPTIONS = ["Continue", "Transfer", "Undecided"]

# Success/Error Messages
SUCCESS_FEEDBACK_SUBMITTED = "Thank you! Your feedback has been submitted successfully."
ERROR_PROGRAM_NAME_REQUIRED = "Please enter your program name."
ERROR_FEEDBACK_REQUIRED = "Please provide some feedback in the open-ended section."
ERROR_SAVE_FEEDBACK = "An error occurred while saving your feedback: {error}"

# Sidebar Content
SIDEBAR_TITLE_FAQ = "Frequently Asked Questions"
SIDEBAR_FAQ_QUESTION = "Why is this feedback important?"
SIDEBAR_FAQ_ANSWER = "Your feedback helps us continuously improve our programs and enhance the learning experience for all Aggies."
SIDEBAR_ANONYMOUS_INFO = "Your responses are anonymous and will be used solely for program improvement purposes."
SIDEBAR_PRIVACY_TITLE = "Data Privacy Notice"
SIDEBAR_PRIVACY_TEXT = """
We value your privacy. All responses are anonymized and securely stored. 
The data collected will only be used for program improvement purposes and will not be shared with third parties.
"""

# Footer
FOOTER_TEXT = "© 2025 Texas A&M University. All rights reserved."


# =============================================================================
# ARKANSAS SCHEDULING POLL STRINGS (app.py)
# =============================================================================

# Page Configuration
ARKANSAS_PAGE_TITLE = "Arkansas Scheduling Poll"

# Header Section
ARKANSAS_TITLE = "📍 Arkansas Onsite Scheduling Poll"
ARKANSAS_INSTRUCTIONS = "Select **any dates** below you are **not available** to travel or attend the in-person event in **Little Rock, AR**."

# Form Labels
LABEL_FULL_NAME = "Full Name"
LABEL_EMAIL_ADDRESS = "Email Address"
LABEL_UNAVAILABLE_DATES = "What dates are you *NOT* available?"
LABEL_COMMENTS = "Optional Comments / Notes"
LABEL_SUBMIT_AVAILABILITY = "Submit Availability"

# Success/Error/Warning Messages
SUCCESS_AVAILABILITY_SUBMITTED = "✅ Your availability has been submitted!"
ERROR_NAME_EMAIL_REQUIRED = "Please provide both your name and email."
WARNING_NO_DATES_SELECTED = "You haven't selected any dates. Are you available all dates?"
ERROR_SUBMISSION_FAILED = "❌ Submission failed: {error}"
ERROR_S3_INIT_FAILED = "Failed to initialize AWS S3: {error}"

# Progress Messages
SPINNER_SUBMITTING = "Submitting your response..."

# Sidebar Content
SIDEBAR_ABOUT_TITLE = "ℹ️ About this Poll"
SIDEBAR_ABOUT_TEXT = """
This poll helps us schedule an in-person event based on staff availability.
Please select any dates you are **not available**.
"""
SIDEBAR_ARKANSAS_PRIVACY_TITLE = "🔒 Data Privacy Notice"
SIDEBAR_ARKANSAS_PRIVACY_TEXT = """
Your responses are confidential and will only be used for internal scheduling purposes.
"""

# Footer
ARKANSAS_FOOTER_TEXT = "© 2025 State of Arkansas Event Coordination Team"
