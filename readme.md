# Bookly

Bookly is an innovative online platform designed for book lovers to connect and share their personal collections. Users can easily list the novels and books they own, making them available for others to purchase or borrow. Whether you’re looking to clear space on your bookshelf, discover new reads, or lend a hand to fellow readers, Bookly creates a community-driven marketplace for exchanging books. With a simple and user-friendly interface, Bookly makes it effortless to explore a wide variety of titles, fostering a sustainable and connected book-sharing experience.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

### Auth

- **User Registration and Authentication:** Users can register, log in, and manage their accounts.
- **Account Activation via Email:** New users receive an activation link to confirm their account.
- **Password Reset Functionality:** Users can request a password reset link via email.
- **Token Blacklisting:** Ensures that tokens are invalidated after logout or expiration.
- **Celery Integration for Background Tasks:** For sending emails and clearing expired tokens and logs.

### Profile

- **Auto User Profile Creation**: User profile is created on user verification.
- **User Profile Update**: Users can update their profile information.
- **Avatar Image Upload**: Users can upload and image through form data to be used as avatar image.

## Technologies Used

- **Backend Framework:** FastAPI
- **Database:** PostgreSQL
- **Asynchronous ORM:** SQLModel
- **Task Queue:** Celery
- **Broker:** Redis
- **Storage:** MinIO
- **Other Libraries:** Pydantic, Alembic, etc.

## Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.9 or higher
- Docker
- Docker Desktop (optional but recommended)

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/datarohit/bookly.git
    cd bookly
    ```

2. **Start the application using Docker Compose:**

    ```bash
    docker-compose up -d --build
    ```

This command will build the necessary services and start the application, including the database, Redis server, and any other dependencies required for the project.

## Usage

- Access the API at `http://localhost:8000/api/v1/`.
- Use the `/auth` endpoints for user authentication and management.

## Modules

### Auth Endpoints

- **Register User:** `POST /auth/register`
- **Activate User:** `POST /auth/activate/{activation_token}`
- **Login User:** `POST /auth/login`
- **Logout User:** `POST /auth/logout`
- **Forgot Password:** `POST /auth/forgot-password`
- **Reset Password:** `POST /auth/reset-password/{password_reset_token}`
- **Get Logged-in User:** `GET /auth/me`

### Profile Endpoints

- **Update Profile:** `PATCH /profile/update-profile`
- **Update Avatar Image**: `PATCH /profile/update-avatar`

## API Documentation

You can find the full API documentation at `http://localhost:8000/api/v1/docs`, generated using Swagger UI.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Make sure to follow the code style and conventions.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/DataRohit/Bookly/blob/master/license) file for more details.

## Contact

For any inquiries or feedback, please contact:

- **Rohit Ingole** - [rohit.vilas.ingole@gmail.com](mailto:rohit.vilas.ingole@gmail.com)
- **GitHub:** [datarohit](https://github.com/datarohit)
