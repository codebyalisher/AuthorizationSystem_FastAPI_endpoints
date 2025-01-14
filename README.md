# AuthorizationSystem2

## Overview
AuthorizationSystem2 is a robust and scalable system designed to manage user authentication and authorization. It leverages modern web technologies to ensure secure and efficient handling of user data and permissions. The system supports features like user registration, email verification, secure login, token-based authentication, and user management.

---

## Project Structure
```
AuthorizationSystem2/
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- config.py
|   |-- models.py
|   |-- schemas/
|   |   |-- auth.py
|   |   |-- user.py
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- auth.py
|   |   |-- user.py
|   |-- utils/
|   |   |-- __init__.py
|   |   |-- send_email.py
|   |-- services/
|       |-- auth_service.py
|       |-- user_service.py
|-- .env
|-- requirements.txt
|-- README.md
```

---

## Flow of the Project
1. **User Registration**
   - Users register through the `/api/v1/users/auth/signup` endpoint by providing necessary details like email and password.
   - Email verification is initiated to validate the user's authenticity.

2. **Email Verification**
   - An email is sent to the user containing a verification link.
   - The user clicks the link to verify their email address.

3. **User Login**
   - Users log in through the `/api/v1/users/auth/signin` endpoint.
   - The system validates user credentials and generates a JWT token upon successful login.

4. **Protected Routes**
   - Users access secure API endpoints by including the JWT token in their requests.

5. **User Management**
   - Admins or authorized users can perform CRUD operations on user data using specific endpoints.

---

## Techniques Used
- **FastAPI**: Framework for building the web API.
- **Pydantic**: Data validation and serialization/deserialization.
- **JWT (JSON Web Tokens)**: Secure token-based authentication.
- **SQLAlchemy**: Database interactions.
- **SMTP**: Email verification functionality.
- **Environment Variables**: For secure storage of sensitive information.

---

## Architecture
AuthorizationSystem2 follows a modular architecture with a clear separation of concerns:
- **Models**: Define the database schema (e.g., User model).
- **Routes**: Handle API endpoints (e.g., authentication and user management).
- **Schemas**: Define request and response models for data validation.
- **Utils**: Provide utility functions (e.g., email sending functionality).
- **Services**: Contain business logic for authentication and user management.

---

## Scenarios
1. **User Registration and Login**
   - Ensures secure user registration and login processes.
2. **Email Verification**
   - Validates the user's email address to confirm authenticity.
3. **Token-Based Authentication**
   - Secures API endpoints by validating JWT tokens.
4. **User Management**
   - Allows CRUD operations for managing user data.

---

## Project Features

### 1. User Registration
- **Development**: Implemented in `routes/auth.py` with validation in `schemas/auth.py`.
- **Integration**: Integrated with the email sending utility in `utils/send_email.py`.
- **Endpoint**: `POST /api/v1/users/auth/signup`

### 2. Email Verification
- **Development**: Implemented in `utils/send_email.py`.
- **Integration**: Integrated into the user registration flow.
- **Endpoint**: `GET /api/v1/users/auth/verify`

### 3. User Login
- **Development**: Implemented in `routes/auth.py`.
- **Integration**: Integrated with JWT token generation and validation.
- **Endpoint**: `POST /api/v1/users/auth/signin`

### 4. Token Refresh
- **Development**: Implemented in `routes/auth.py`.
- **Integration**: Ensures secure and refreshed access for authenticated users.
- **Endpoint**: `POST /api/v1/users/auth/refresh-token`

### 5. User Management (CRUD Operations)
- **Development**: Implemented in `routes/user.py` with validation in `schemas/user.py`.
- **Endpoints**:
  - Create User: `POST /api/v1/users/data/create-user`
  - Update User: `PUT /api/v1/users/data/update-user`
  - Get User by ID: `GET /api/v1/users/data/get-user-byid`
  - Get All Users: `GET /api/v1/users/data/get-all-users`
  - Delete User by ID: `DELETE /api/v1/users/data/delete-user-byid`

---

## Endpoints
### Authentication Endpoints
- **User Registration**: `POST http://127.0.0.1:8000/api/v1/users/auth/signup`
- **Email Verification**: `GET http://127.0.0.1:8000/api/v1/users/auth/verify`
- **User Login**: `POST http://127.0.0.1:8000/api/v1/users/auth/signin`
- **Token Refresh**: `POST http://127.0.0.1:8000/api/v1/users/auth/refresh-token`
- **Get Current User**: `GET http://127.0.0.1:8000/api/v1/users/auth/me`

### User Management Endpoints
- **Create User**: `POST http://127.0.0.1:8000/api/v1/users/data/create-user`
- **Update User**: `PUT http://127.0.0.1:8000/api/v1/users/data/update-user`
- **Get User by ID**: `GET http://127.0.0.1:8000/api/v1/users/data/get-user-byid`
- **Get All Users**: `GET http://127.0.0.1:8000/api/v1/users/data/get-all-users`
- **Delete User by ID**: `DELETE http://127.0.0.1:8000/api/v1/users/data/delete-user-byid`

---

## How to Use This Project

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd AuthorizationSystem2
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file and add necessary environment variables (e.g., `DATABASE_URL`, `SECRET_KEY`, `EMAIL_CREDENTIALS`).

5. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API**:
   - Open your browser or API testing tool (e.g., Postman) and navigate to `http://127.0.0.1:8000`.

7. **Test Endpoints**:
   - Use the provided endpoints to test user registration, login, email verification, and user management functionalities.

