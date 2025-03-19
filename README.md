# VyomFaceAuthentication
A Flask API for face authentication, containerized with Docker and deployed on Google Cloud Run for scalable and serverless operation.
# Face Authentication API - Deployed on Google Cloud Run

This repository contains the source code for a robust and scalable Face Authentication API. It's built using the Python Flask framework and deployed on Google Cloud Run through Docker containerization. This serverless deployment ensures that your API can handle varying loads efficiently and reliably.

## Project Overview

The primary goal of this API is to provide secure and accurate facial authentication services. It allows users to verify their identity by comparing uploaded facial images against a database of registered profiles. By leveraging Docker and Google Cloud Run, we've created a system that's easy to deploy, scale, and maintain.

## Key Technologies

* **Flask:** A lightweight and flexible Python web framework, chosen for its simplicity and efficiency in API development.
* **Docker:** Used to containerize the application, ensuring consistent environments across development and production.
* **Google Cloud Run:** Provides a serverless platform for deploying the Docker container, enabling automatic scaling and pay-per-use billing.
* **Python:** The core programming language, selected for its rich ecosystem and ease of use in web development.

## Getting Started - Local Development

To get the API running on your local machine for development or testing:

1.  **Prerequisites:** Ensure you have Python and Docker installed.
2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/adnankhan171/VyomFaceAuthentication
    ```
3.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
4.  **Activate the Virtual Environment:**
    * On Windows:
        ```bash
        venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Run the Flask Application:**
    ```bash
    python app.py
    ```
7.  **Run the Docker Container Locally:**
    ```bash
    docker build -t face-auth-api .
    docker run -p 5000:5000 face-auth-api
    ```

## Deployment to Google Cloud Run

This API is designed for deployment on Google Cloud Run. The process involves:

1.  **Building the Docker Image:** Using the provided `Dockerfile`.
2.  **Pushing the Image:** To Google Container Registry (GCR).
3.  **Deploying to Cloud Run:** Configuring and deploying the service through the Google Cloud Console or the `gcloud` command-line tool.

For detailed deployment instructions, please refer to the Google Cloud Run documentation.

## Contributing

We welcome contributions to improve this API. If you find a bug, have a feature request, or want to contribute code.