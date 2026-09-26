# AWS Resource Manager

This project implements a distributed resource-allocation workflow using Python, Flask, Amazon SQS, Amazon DynamoDB, and AWS Lambda.

Three user services submit resource-allocation decisions to an SQS queue. AWS Lambda functions collect and aggregate those decisions from DynamoDB, then send the combined results to a central Flask resource manager. The resource manager calculates time and cost values and returns the results to the user services.

## Project structure

### `resource_manager.py`

Runs the central Flask service. It exposes a `POST /compute` endpoint that:

1. Receives allocation matrices and timing data.
2. Calculates total resource time and estimated cost.
3. Sends the results to the three user services.

### `user1.py`, `user2.py`, and `user3.py`

Run the three user-side Flask services. Each service exposes a `POST /start` endpoint, calculates a resource-allocation strategy, submits it through SQS, and processes the aggregated results returned by the resource manager.

### `users_functions.py`

Contains the shared allocation and utility logic used by the three user services, including constraint checking, utility calculations, matrix generation, and SQS submission.

### `utilities.py`

Stores shared project parameters such as the number of users, number of resources, resource prices, timing estimates, and task constraints.

### `config.py`

Loads local configuration from `.env` during development and reads environment variables when the application is deployed. AWS Lambda functions should receive their configuration through Lambda environment variables.

### `lamdas/GetAllocationVectors.txt`

AWS Lambda handler that consumes SQS records and stores user allocation vectors and timing data in the DynamoDB table.

### `lamdas/GetnSet.txt`

AWS Lambda handler triggered by DynamoDB events. It waits until all user submissions for a round are available, sends the combined payload to the resource manager, and marks the round as processed.

The Lambda files currently use a `.txt` extension for documentation/storage. Rename them to `.py` when packaging them for AWS Lambda.

### `report.pdf` and `Bonus.pdf`

Assignment documentation and related supporting material.

## Technologies

- Python
- Flask
- Boto3
- Amazon SQS
- Amazon DynamoDB
- AWS Lambda
- Requests
- urllib3

## Configuration

Copy the example configuration file and replace the placeholders:

```powershell
Copy-Item .env.example .env
```

The local `.env` file contains deployment-specific endpoints and is ignored by Git. Do not commit it or share it publicly.

AWS access credentials should be provided through the AWS CLI profile, environment variables, an IAM role, or the Lambda execution role. Do not place AWS access keys in this repository.

## Local setup

Create and activate a virtual environment, then install the required packages:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask requests boto3 urllib3
```

Start the services separately, using different ports when running them on the same machine:

```powershell
python resource_manager.py
python user1.py
python user2.py
python user3.py
```

The default Flask port is `5000`; update the service configuration if multiple services run on one host.

## Project status

This is an academic distributed-systems project. It is not production-ready and requires AWS resources, correct IAM permissions, compatible Lambda triggers, network reachability between services, and deployment-specific testing.

