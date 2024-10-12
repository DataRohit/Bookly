# Bookly FastAPI Backend

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

### Book Category

- **Create and Update:** User can create new categories and update the categories created by them.
- **Get and List:** Users can list all categories or get a specific category details by category name.

### Book Genre

- **Create and Update:** User can create new categories and update the categories created by them.
- **Get and List:** Users can list all categories or get a specific genre details by genre name.

### Book

- **Create Book:** Users can submit a book for sharing, including details such as title, author, description, category and genre.
- **Update Book:** Users can modify existing book details, including the description and other attributes.
- **List Books:** Users can view a comprehensive list of all books posted by all users in a user-friendly format.
- **Get Book By ISBN:** Users can retrieve a book's details by entering its unique ISBN number for precise identification.
- **Get Book By UID:** Users can access specific book information using the unique identifier (UID) assigned to each book.
- **Get Book By Title:** Users can search for books by entering the title for quick access to relevant titles.
- **List Books by Category:** Users can browse books organized by predefined categories for easier navigation.
- **List Books by Genre:** Users can explore books categorized by genre, making it simple to find specific types of literature.
- **List Books by Author:** Users can filter and view books authored by a specific individual, streamlining the search for fans.
- **Update Book Images:** Users can upload or replace images for a book, with a maximum limit of five images per book.

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

### Book Category Endpoints

- **Create Category:** `POST /books/category/create`
- **Update Category:**  `PATCH /books/category/update/{category_uid}`
- **Get Category By Category Name:** `GET /books/category/get/{category}`
- **List All Categories:** `GET /books/category/list`

### Book Genre Endpoints

- **Create Genre:** `POST /books/genre/create`
- **Update Genre:**  `PATCH /books/genre/update/{genre_uid}`
- **Get Genre By Genre Name:** `GET /books/genre/get/{genre}`
- **List All Categories:** `GET /books/genre/list`

### Book Endpoints

- **Create Book:** `POST /books/create`
- **Update Book:** `PATCH /books/update/{book_uid}`
- **List Books:** `GET /books/list`
- **Get Book By ISBN:** `GET /books/get/isbn/{isbn}`
- **Get Book By UID:** `GET /books/get/uid/{book_uid}`
- **Get Book By Title:** `GET /books/get/title/{title}`
- **List Books by Category:** `GET /books/list/category/{category}`
- **List Books by Genre:** `GET /books/list/genre/{genre}`
- **List Books by Author:** `GET /books/list/author/{author}`
- **Update Book Images:** `PATCH /update/images/{book_uid}`

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
