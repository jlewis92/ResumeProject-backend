# ResumeProject-backend
Back end work for the [AWS cloud resume challenge](https://cloudresumechallenge.dev/docs/the-challenge/aws/)

This repository consists of 2 parts: A python lambda expression and a terraform project used within the backend of the project.

## Python
The python code in this repository makes use of the boto3 library to get and update a value in a dynamodb table for a visitor counter used in the [frontend](https://github.com/jlewis92/ResumeProject-frontend) of this project.  In terms of testing, the project makes use of moto to mock calls to AWS.

## Terraform
This project makes use of terraform for the following actions:

 - Build and sync the lambda expression related to the above python code
 - Generate a dynomdb table
 - Create an api gateway and integration for the above lambda, including CORS headers
 - Generate AWS policies and roles linking the resources together
 - Setup a github actions OIDC token and role for use with running builds related to this resume project

## Build
This project makes use of github actions to automate the build and deployment of the backend for this resume project.  In particulaer, this build will automatically run python tests written for this project and then verify the terraform by performing terraform format, validate and plan actions.  Within pull requests a bot will update the pull request with an overview of how the build went for terraform, as well as an overview of the plan.  When run on the main branch, a terraform apply will also be carried out.  All actions within AWS are completed using a github OIDC token

Finally, git pre-commits are used to remove trailing whitespace, format terraform and verify there are no plaintext secrets within the project
