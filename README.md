# User Management API with Flask and MySQL

This project implements a RESTful API for managing user data using Flask and MySQL. It provides CRUD operations for user records and is containerized using Docker for easy deployment and scalability.

The User Management API allows you to create, read, update, and delete user records in a MySQL database. It's built with Flask, a lightweight Python web framework, and uses MySQL Connector for Python to interact with the database. The application is containerized using Docker, making it easy to set up and run in various environments.

Key features of this API include:
- User creation with name and email
- Retrieval of all users or a specific user by ID
- Updating user information
- Deleting user records
- Containerized application and database using Docker Compose

## Repository Structure

```
.
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── server.py
```

- `docker-compose.yml`: Defines the multi-container Docker application, including the web service and MySQL database.
- `Dockerfile`: Contains instructions for building the Docker image for the Flask application.
- `requirements.txt`: Lists the Python dependencies required for the project.
- `server.py`: The main Flask application file containing the API endpoints and database operations.

## Usage Instructions

### Prerequisites

- Docker and Docker Compose installed on your system
- Git (optional, for cloning the repository)

### Installation

1. Clone the repository or download the project files:

   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker image for the Flask application and start both the web service and the MySQL database.

3. The API will be available at `http://localhost:8080`.

### API Endpoints

- `GET /users`: Retrieve all users
- `GET /users/<user_id>`: Retrieve a specific user by ID
- `POST /users`: Create a new user
- `PUT /users/<user_id>`: Update an existing user
- `DELETE /users/<user_id>`: Delete a user

### Example Usage

#### Create a new user

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com"}' http://localhost:8080/users
```

#### Retrieve all users

```bash
curl http://localhost:8080/users
```

#### Retrieve a specific user

```bash
curl http://localhost:8080/users/1
```

#### Update a user

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Jane Doe"}' http://localhost:8080/users/1
```

#### Delete a user

```bash
curl -X DELETE http://localhost:8080/users/1
```

### Troubleshooting

1. Database Connection Issues:
   - Problem: The Flask application cannot connect to the MySQL database.
   - Solution: 
     - Ensure the MySQL container is running: `docker-compose ps`
     - Check the environment variables in `docker-compose.yml` match the database configuration
     - Verify network connectivity between containers: `docker network inspect <network-name>`

2. API Endpoint Not Responding:
   - Problem: Requests to API endpoints return a connection refused error.
   - Solution:
     - Confirm the Flask application is running: `docker-compose logs web`
     - Ensure the correct port is exposed in the Dockerfile and mapped in docker-compose.yml
     - Check if the application is listening on all interfaces (0.0.0.0)

3. Data Persistence Issues:
   - Problem: Data is lost when containers are restarted.
   - Solution:
     - Verify the MySQL data volume is correctly configured in docker-compose.yml
     - Check if the volume is created and mounted: `docker volume ls` and `docker inspect <volume-name>`

### Performance Optimization

- Monitor database query performance using MySQL's slow query log
- Implement database indexing on frequently queried fields
- Use connection pooling for database connections to reduce overhead
- Consider implementing caching for frequently accessed data

## Data Flow

The User Management API follows a simple request-response flow:

1. Client sends an HTTP request to one of the API endpoints.
2. The Flask application receives the request and routes it to the appropriate function.
3. The function establishes a connection to the MySQL database.
4. The function executes the necessary SQL query or command.
5. The database returns the result to the Flask application.
6. The Flask application processes the result and constructs a JSON response.
7. The JSON response is sent back to the client.

```
Client <-> Flask Application <-> MySQL Database
   |             |                    |
   |  HTTP       |   SQL Queries      |
   |  Request    |    and Results     |
   |             |                    |
   |  JSON       |                    |
   |  Response   |                    |
   |             |                    |
```

Note: The Flask application and MySQL database are running in separate Docker containers, which allows for easy scaling and management of each component independently.

## Infrastructure

The project uses Docker Compose to define and run the multi-container Docker application. The infrastructure consists of two main components:

1. MySQL Database (Service: db)
   - Image: mysql:8
   - Environment variables for database configuration
   - Persistent volume for data storage

2. Web Application (Service: web)
   - Custom-built Docker image based on the project's Dockerfile
   - Exposes port 8080
   - Environment variables for database connection
   - Depends on the db service

The `docker-compose.yml` file defines these services and their configurations, ensuring that the application and database are properly linked and can communicate with each other.