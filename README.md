# Delivery Parcel Management System

## Objective

The objective of this project is to develop a delivery parcel management system that tracks and manages parcels from reception to delivery using dummy data. The system will enable users to add, update, track, and report on parcel status and provide real-time updates on long-running tasks, such as bulk parcel processing.

## Technologies Used

- **HTML/CSS**: For structuring and styling the user interface of the application.
- **JavaScript**: To implement dynamic features and client-side logic.
- **Bootstrap**: For designing responsive and modern web layouts quickly.
- **jQuery**: To simplify HTML document manipulation, event handling, and AJAX interactions.
- **Python**: For server-side logic and interaction with the database.
- **Flask**: A lightweight web framework to handle HTTP requests and deliver web pages.
- **SocketIO (Flask-SocketIO)**: To enable real-time bidirectional communication between web clients and servers.
- **Pandas**: For handling bulk data operations and transformations.
- **SQL (MySQL)**: To store and manage application data like user and parcel information.

## Project Breakdown

### 1. Database Setup

- Design a MySQL database for storing users, parcels, and transaction logs.
- Implement secure user authentication and role-based access control.

### 2. Backend Development

- Configure the Flask server and API routes for parcel data operations.
- Integrate Flask-SocketIO for real-time progress updates.

### 3. Frontend Development

- Use HTML, CSS, and Bootstrap to build the user interface.
- Implement JavaScript and jQuery for dynamic content updates and API communication.
- Set up real-time communication with Flask-SocketIO, including showing loaders for backend tasks like processing parcels.
- Design Section:
  - **Template Dashboard for UI Design**: Utilize the Sneat Bootstrap HTML Admin Template for a cohesive look.
  - **Single Page Application (SPA)**: Implement the main functionalities on a single page to simplify user interaction.
  - **Multiple Pages**: Optionally, add more pages if necessary to separate detailed functionalities.

### 4. Data Processing

- Use Pandas for data manipulation during bulk operations or reports.

### 5. Documentation

- Document the setup process, API usage, and general system operations.

## Deliverables

- **GitHub**: The complete codebase for the project will be managed using Git and hosted on GitHub. The project will include:
  - Source code
  - Database schema
  - Installation and setup instructions
  - API documentation
  - User guide for the application

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask-SocketIO
- Pandas
- MySQL
- Node.js and npm (for managing frontend dependencies)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Karan7426/Parcel-manager-system

2. Navigate to the project directory:
   ```bash
    composer install
    ```
3. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows use `venv\Scripts\activate`
```
4. Install the Python dependencies:
    ```bash
   pip install -r requirements.txt
5. Set up the MySQL database and configure the connection settings in config.py
  
   -Create the Database:
         ```bash
          CREATE DATABASE parcel_management;
          USE parcel_management;
         ```
   -Tables
    ```bash
    CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    is_admin TINYINT(1) DEFAULT 0,  
   );
    CREATE TABLE parcel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    parcel_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    estimated_date DATE NULL,
    location VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
      ```
- Configure Database Connection:
```bash
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/parcel_management'
```

6.Run the Flask application:
```bash
python app.py
```

7.
- Example SQL for Creating Admin User:
```bash
INSERT INTO user (username, password, email, is_admin) VALUES ('admin', 'your_hashed_password', 'admin@example.com', 1);
```
7.
- Example SQL for Creating Normal User:
```bash
INSERT INTO user (username, password, email, is_admin) VALUES ('username', 'your_hashed_password', 'user@example.com', 0);


