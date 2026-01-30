"""
Environment-based configuration for the feedbacksolution application.
This module centralizes all configuration values that may change between deployments.
Environment variables are used with sensible defaults for backwards compatibility.
"""

import os


# =============================================================================
# AWS CONFIGURATION
# =============================================================================

# AWS credentials are read directly from standard AWS environment variables
# by the boto3 client: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

# Default AWS region (used when AWS_DEFAULT_REGION is not set)
DEFAULT_AWS_REGION = os.getenv("DEFAULT_AWS_REGION", "us-east-1")


# =============================================================================
# ARKANSAS SCHEDULING POLL (app.py) CONFIGURATION
# =============================================================================

# Enable/disable S3 storage (set to "false" to save locally instead)
APP_USE_S3 = os.getenv("APP_USE_S3", "true").lower() == "true"

# S3 bucket name for scheduling poll responses
APP_S3_BUCKET_NAME = os.getenv("APP_S3_BUCKET_NAME", "awsbin-arkansasonline-poll")

# S3 key prefix for scheduling data
APP_S3_KEY_PREFIX = os.getenv("APP_S3_KEY_PREFIX", "scheduling")

# Application name (used in titles and metadata)
APP_NAME = os.getenv("APP_NAME", "Arkansas Scheduling Poll")

# Environment name (e.g., "development", "staging", "production")
APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "production")


# =============================================================================
# STUDENT FEEDBACK FORM (studentfeedback_app.py) CONFIGURATION
# =============================================================================

# S3 bucket name for student feedback responses
FEEDBACK_S3_BUCKET_NAME = os.getenv("FEEDBACK_S3_BUCKET_NAME", "awsbin-amazonq-assets")

# Application name for feedback form
FEEDBACK_APP_NAME = os.getenv("FEEDBACK_APP_NAME", "Texas A&M Student Feedback Form")

# Organization name (used in footer copyright)
FEEDBACK_ORGANIZATION = os.getenv("FEEDBACK_ORGANIZATION", "Texas A&M University")

# Environment name
FEEDBACK_ENVIRONMENT = os.getenv("FEEDBACK_ENVIRONMENT", "production")


# =============================================================================
# EXTERNAL URLS (if needed)
# =============================================================================

# Logo/image URL (can be overridden for different deployments)
FEEDBACK_LOGO_PATH = os.getenv("FEEDBACK_LOGO_PATH", "./primaryTAM.png")


# =============================================================================
# FEATURE FLAGS
# =============================================================================

# Enable/disable balloons animation on successful submission
ENABLE_BALLOONS = os.getenv("ENABLE_BALLOONS", "true").lower() == "true"

# Enable/disable progress bar animation
ENABLE_PROGRESS_BAR = os.getenv("ENABLE_PROGRESS_BAR", "true").lower() == "true"
