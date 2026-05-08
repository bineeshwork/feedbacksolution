# Student Feedback and Scheduling Solution

This project contains two Streamlit-based web applications deployed on AWS infrastructure using CDK:

1. **Texas A&M Student Feedback Form** - Collects structured student feedback for academic programs
2. **Arkansas Onsite Scheduling Poll** - Manages scheduling availability for an onsite event in Little Rock, AR

Both applications are deployed as containerized services with user authentication and cloud storage.

## Architecture

The solution deploys the following components:

* Streamlit applications running in ECS/Fargate, behind an ALB and CloudFront
* A Cognito user pool for user authentication
* S3 buckets for storing form submissions
* Amazon Bedrock integration for generative AI capabilities

![Architecture diagram](img/archi_streamlit_cdk.png)

## Applications

### Student Feedback Form (`docker_app/studentfeedback_app.py`)

A Texas A&M branded feedback collection form that captures:

* Program name
* Course satisfaction (1-5 scale)
* Learning outcomes
* Support services
* Engagement level
* Improvement areas
* Open-ended feedback
* Future plans
* Strengths and weaknesses

Responses are stored as JSON in the S3 bucket `awsbin-amazonq-assets`.

### Arkansas Onsite Scheduling Poll (`docker_app/app.py`)

A scheduling poll for an onsite event in Little Rock, AR that collects:

* Name and email
* Unavailable dates (August-October range)
* Comments

Responses are stored in the S3 bucket `awsbin-arkansasonline-poll`.

## Project Structure

```
.
├── app.py                      # CDK app entry point
├── cdk/
│   └── cdk_stack.py            # CDK infrastructure stack
├── cdk.json                    # CDK configuration
├── docker_app/
│   ├── app.py                  # Arkansas Scheduling Poll (Streamlit)
│   ├── studentfeedback_app.py  # Student Feedback Form (Streamlit)
│   ├── config_file.py          # Application configuration
│   ├── Dockerfile              # Container configuration
│   ├── docker-compose.yml      # Docker Compose config
│   ├── requirements.txt        # App Python dependencies
│   ├── primaryTAM.png          # Texas A&M logo
│   └── utils/
│       ├── auth.py             # Authentication utilities
│       └── llm.py              # Bedrock LLM utilities
├── img/                        # Architecture diagrams
├── tests/                      # Unit tests
├── requirements.txt            # CDK/deployment dependencies
└── requirements-dev.txt        # Dev dependencies
```

## Configuration

The application configuration is in `docker_app/config_file.py`:

* `STACK_NAME` = "StudentFeedback"
* `DEPLOYMENT_REGION` = "us-east-1"
* `BEDROCK_REGION` = "us-east-1"
* Cognito authentication via AWS Secrets Manager

## Usage

### Prerequisites

* Python >= 3.8
* Docker
* AWS CLI configured with appropriate credentials
* AWS CDK installed
* `anthropic.claude-v2` model activated in Amazon Bedrock in your AWS account
* A Chrome browser is recommended for development

The environment used to create this demo was an AWS Cloud9 m5.large instance with Amazon Linux 2023, but it should also work with other configurations. It has also been tested on a Mac laptop with colima as container runtime.

You also need to install the AWS Command Line Interface (CLI), the AWS Cloud Development Kit (CDK), and configure the AWS CLI on your development environment (not required if you use Cloud9, as it is already configured by default).

### Deployment

1. Edit `docker_app/config_file.py` to update configuration as needed (stack name, regions, secrets).

2. Install dependencies:

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Deploy the CDK template:

```
cdk bootstrap
cdk deploy
```

The deployment takes 5 to 10 minutes.

Make a note of the output, in which you will find the CloudFront distribution URL
and the Cognito user pool id.

4. Create a user in the Cognito UserPool that has been created. You can perform this action from your AWS Console.
5. From your browser, connect to the CloudFront distribution URL.
6. Log in to the Streamlit app with the user you have created in Cognito.

### Running Locally

After deployment of the CDK template (which creates the Cognito user pool required for authentication), you can test the Streamlit apps directly.

1. If you have activated a virtual env for deploying the CDK template, deactivate it:

```
deactivate
```

2. Change into the docker_app directory, create a new virtual env, and install dependencies:

```
cd docker_app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Launch the scheduling poll app:

```
streamlit run app.py --server.port 8080
```

Or launch the student feedback app:

```
streamlit run studentfeedback_app.py --server.port 8080
```

4. If using Cloud9, click on the Preview/Preview running application button, and pop out the browser in a new window (the embedded browser does not keep session cookies, which prevents authentication from working properly).

## Some Limitations

* The connection between CloudFront and the ALB is in HTTP, not SSL encrypted.
This means traffic between CloudFront and the ALB is unencrypted.
It is **strongly recommended** to configure HTTPS by bringing your own domain name and SSL/TLS certificate to the ALB.
* The provided code is intended as a demo and starting point, not production ready.
The Python app relies on third party libraries like Streamlit and streamlit-cognito-auth.
As the developer, it is your responsibility to properly vet, maintain, and test all third party dependencies.
The authentication and authorization mechanisms in particular should be thoroughly evaluated.
More generally, you should perform security reviews and testing before incorporating this demo code in a production application or with sensitive data.
* In this demo, Amazon Cognito is in a simple configuration.
Note that Amazon Cognito user pools can be configured to enforce strong password policies,
enable multi-factor authentication,
and set the AdvancedSecurityMode to ENFORCED to enable the system to detect and act upon malicious sign-in attempts.
* AWS provides various services, not implemented in this demo, that can improve the security of this application.
Network security services like network ACLs and AWS WAF can control access to resources.
You could also use AWS Shield for DDoS protection and Amazon GuardDuty for threats detection.
Amazon Inspector performs security assessments.
There are many more AWS services and best practices that can enhance security -
refer to the AWS Shared Responsibility Model and security best practices guidance for additional recommendations.
The developer is responsible for properly implementing and configuring these services to meet their specific security requirements.
* Regular rotation of secrets is recommended, not implemented in this demo.

## Acknowledgments

This code is inspired from:

* https://github.com/tzaffi/streamlit-cdk-fargate.git
* https://github.com/aws-samples/build-scale-generative-ai-applications-with-amazon-bedrock-workshop/

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This application is licensed under the MIT-0 License. See the LICENSE file.
