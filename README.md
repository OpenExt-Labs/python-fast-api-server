# FastAPI Server Tutorial

This tutorial will guide you through the setup, installation, and usage of the FastAPI server with consistent response models.

## Table of Contents

1. [Introduction](#introduction)
2. [Setup and Installation](#setup-and-installation)
3. [Response Models](#response-models)
4. [API Endpoints](#api-endpoints)
5. [Running the Server](#running-the-server)
6. [Testing the Endpoints](#testing-the-endpoints)

## Introduction

This FastAPI server uses a consistent response structure for all API endpoints, ensuring that responses always include `error`, `message`, and `data` fields. This structure improves the API's usability and makes it easier to handle responses on the client side.

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Poetry for dependency management

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/fastapi-server.git
   cd fastapi-server
   ```
2. **Install dependencies:**

   ```sh
   poetry install
   ```

3. **Create a `.env` file:**

   ```sh
   touch .env.local
   ```
   Example .env.local content:
    ```sh
    MYSQL_ROOT_PASSWORD=
    MYSQL_DATABASE=
    MYSQL_USER=
    MYSQL_PASSWORD=
    MYSQL_HOST=
    MYSQL_PORT=
    PROFILER_SECRET_P=9383273

    ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzYW5nbGUxIiwiZXhwIjoxNzE4MjA0OTE3fQ.rH7Ux72gfZCCfErDW_YzdG4A9BhOidFszPRoFN-w6K0
    INVALID_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.z-jTfyTJX1V3kEfdiq824clRo_WbSmuPhm5mLvu5F5E
    ```

### Running the Server
```sh
poetry run uvicorn src.main:app --reload
```
- The server will start running at `http://localhost:8000`.
- You can access the API documentation at `http://localhost:8000/docs`.
- Profiler will be available at `http://localhost:8000/profiler?p=`.
   
