<<<<<<< HEAD
# Know Your Stocks

## Introduction
Know Your Stocks is a Python-based web application backend designed to provide users with stock market insights and notifications. The application allows users to track their favorite stocks, receive real-time updates, and analyze market trends.

## Features
- **User Authentication:** Users can sign up, log in, and manage their accounts securely.
- **Stock Tracking:** Users can add their favorite stocks to their watchlist and receive updates on stock prices and trends.
- **Real-time Notifications:** Users can receive notifications via email for significant changes in stock prices or market trends.


## Setup Instructions
1. **Create a Python Virtual Environment:**
    ```bash
    python -m venv venv
    ```

2. **Activate the Virtual Environment:**
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

3. **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Create Environment Variables File (.env):**
    - Create a file named `.env` in the root directory.
    - Add the following environment variables and replace the placeholder values with your credentials:
        ```plaintext
        CLIENT_ID=your_google_auth_client_id
        CLIENT_SECRET=your_google_auth_client_secret
        SENDER_EMAIL=your_sender_email
        SENDER_PASSWORD=your_sender_email_password
        ```

5. **Run Django Server:**
    ```bash
    python manage.py runserver
    ```

6. **Access the Application:**
    - Open your web browser and navigate to `http://localhost:8000` to access the application.

## Technologies Used
- Python
- Django
- HTML
=======
#know your stocks
>>>>>>> 837123640734c9b350a4f3b13c896c6aca9cc7da
