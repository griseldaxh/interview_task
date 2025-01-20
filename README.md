# Amazon Product Insights

This project provides a system to collect, analyze, aggregate, and display product insights for Amazon products. The system uses **FastAPI** as the backend, which exposes endpoints to retrieve aggregated insights, and **React** as the frontend for displaying the data. The data processing pipeline is designed to collect product data, analyze it using sentiment analysis and issue extraction, and then aggregate the insights before storing them in a database.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Data Pipeline Overview](#data-pipeline-overview)
- [Key Decisions and Trade-offs](#key-decisions-and-trade-offs)
- [Future Improvements](#future-improvements)
- [Prerequisites](#prerequisites)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
- [Docker Setup for PostgreSQL](#docker-setup-for-postgresql)
- [Testing the API](#testing-the-api)
- [Optional Enhancements](#optional-enhancements)

---

## Architecture Overview

The system is structured to decouple the FastAPI backend from the data processing pipeline, allowing for scalability, maintainability, and performance optimization. Here is a high-level breakdown of the system architecture:

1. **Backend (FastAPI)**:

   - FastAPI serves as the web framework that exposes RESTful API endpoints for product insights and data retrieval.
   - The backend interacts with a PostgreSQL database to store and retrieve product data and aggregated insights.
   - **Endpoints** are designed to fetch:
     - Product insights (`/api/v1/product/{product_id}`)
     - A list of products with pagination (`/api/v1/products`)
   - The backend runs independently and it is optimized to run the pipeline automatically at scheduled intervals using cron jobs or Airflow:
     - Cron Jobs can be used to schedule periodic execution of the data pipeline at specified times (e.g., daily, weekly).
     - Airflow can be integrated to manage complex data processing tasks, workflows, and dependencies. Airflow provides better monitoring, retries, and management of asynchronous workflows.

2. **Data Processing Pipeline**:

   - The data processing pipeline is **modularized** into separate components that handle data collection, sentiment analysis, and insights aggregation.
   - The pipeline processes data asynchronously, collecting reviews, analyzing sentiment, and aggregating insights into useful metrics (e.g., sentiment distribution, common issues).
   - The pipeline can be triggered manually via an API endpoint or scheduled using **cron jobs** or **Celery** for periodic execution.
   - **Separation of concerns**: Each data processing task is modular, ensuring that the code is easy to maintain, test, and extend.

3. **PostgreSQL Database**:

   - PostgreSQL is used as the relational database to store raw product data, reviews, and aggregated insights.
   - The database is containerized using **Docker** for easier management and isolation from the local environment.
   - **SQLAlchemy** is used to handle the database models and interactions.

4. **Frontend (React)**:
   - A **React** application serves as the user interface for displaying the product insights.
   - The frontend communicates with the FastAPI backend using **Axios** for HTTP requests.
   - The frontend provides features like:
     - Displaying product insights
     - Pagination for navigating through large datasets
     - Displaying a list of products and their aggregated insights

---

## Data Pipeline Overview

The data pipeline handles all the data processing tasks in the system, from data collection to analysis and aggregation. It operates asynchronously and is designed to be scalable, robust, and modular. The pipeline has the following stages:

### 1. Data Collection

- Collects raw product data and reviews, either from local files (e.g., JSON) or external data sources
- The pipeline parses the data and prepares it for analysis

### 2. Sentiment Analysis and Issue Extraction

- Analyzes each review for sentiment (positive, negative, neutral) and identifies common issues based on the review content
- This stage uses an LLM (such as OpenAI's GPT) or a custom sentiment analysis model

### 3. Aggregation of Insights

- Aggregates the sentiment analysis results and extracts key insights such as:
  - The percentage of positive, negative, and neutral reviews
  - The top issues or features mentioned in the reviews
- These aggregated insights are then stored in the database for querying and visualization

---

## Key Decisions and Trade-offs

### 1. **Separation of Backend and Data Processing Pipeline**

- **Decision**: The data processing pipeline is decoupled from the FastAPI backend, allowing for better scalability, modularity, and flexibility in how and when the pipeline is triggered. This separation enables the backend to focus solely on handling user requests and serving the API, while the data processing can run independently, either on demand or on a scheduled basis (e.g., using cron jobs or Airflow).
- **Trade-off**:
  - The data processing pipeline is not synchronous with API requests. As a result, API calls that require processed data (like product insights) may require the pipeline to be triggered either manually via the API or scheduled to run periodically (e.g., via cron jobs or Airflow).
  - Complexity is introduced by having to manage external tools (like cron jobs or Airflow) for automating the data processing. This means setting up scheduling, ensuring the pipeline runs correctly, and handling possible failures (which are often automated in these tools).
  - However, this approach prevents blocking API requests, ensuring that the FastAPI backend can remain responsive to user requests, even while the pipeline is running asynchronously in the background or on a scheduled basis.

### 2. **Database Choice (PostgreSQL)**

- **Decision**: PostgreSQL is chosen as the relational database for storing structured data, including product insights and reviews. It is a robust and reliable database that supports complex queries, joins, and ACID compliance, making it ideal for transactional data in this system.
- **Trade-off**:
  - **_Setup and Maintenance Complexity_**: PostgreSQL introduces additional setup complexity, especially when running it inside a Docker container. Dockerizing the database requires proper configuration of volumes, port mappings, and management of container lifecycles (starting, stopping, backing up). Additionally, handling database migrations and ensuring data integrity in Dockerized environments adds overhead compared to running PostgreSQL directly on the host machine.
  - **_Performance Overhead_**: While PostgreSQL is known for reliability, running it inside a container can introduce some performance overhead due to the virtualization layer. This is a trade-off when opting for Dockerization to ensure portability and easier environment management.
  - **_Benefits_**: Despite the added complexity, PostgreSQL provides strong ACID compliance (ensuring consistency, isolation, and durability), scalability (handling large volumes of data), and reliability for transactional data. This makes it well-suited for applications requiring complex queries, data integrity, and long-term storage of insights.

### 3. **Sentiment Analysis and Issue Extraction**

- **Decision**: Use a Large Language Model (LLM), such as OpenAI’s GPT, for sentiment analysis and issue extraction from product reviews. LLMs like GPT are highly effective at understanding the nuances of human language, making them well-suited for extracting sentiment (positive, negative, or neutral) and identifying issues or features mentioned in customer reviews.
- **Trade-off**:
  - **_Cost_**: Using an LLM, especially for analyzing large volumes of data, can incur high operational costs. OpenAI’s GPT charges based on the number of tokens processed, and with a large number of reviews or products, this can become a significant expense.
  - **_Latency_**: The process of calling an external API like OpenAI’s for sentiment analysis introduces latency in the system, particularly when processing a large number of product reviews. This may lead to slower processing times and delays in getting real-time insights, especially when the reviews need to be processed in real-time or near-real-time.
  - **_Optimizations_**:
    - Batch Processing: To mitigate high costs and latency, batch processing has been implemented. Instead of making individual API calls for each review, multiple reviews can be processed in batches, reducing the number of API calls and improving throughput.
    - Asynchronous Calls: The sentiment analysis process is handled asynchronously to avoid blocking other operations. This ensures that the backend can continue to serve API requests while the sentiment analysis runs in the background. This approach minimizes the impact of API latency on the user experience.
  - **_Scalability_**: Although LLMs provide powerful analysis, their usage at scale requires careful management of costs, batch processing, and parallel execution to maintain performance while avoiding excessive resource consumption.

### 4. **Frontend Framework (React)**

- **Decision**: React is used for building the user interface due to its component-based architecture, flexibility, and rich ecosystem. React allows for the creation of reusable components, making it easier to build and maintain large, complex UIs. Additionally, its wide adoption and extensive library ecosystem (including tools like Redux, React Router, and Material-UI) provide powerful solutions for state management, routing, and styling.
- **Trade-off**:
  - **_Performance Overhead_**: React’s virtual DOM and re-rendering mechanism are generally optimized for performance, but for very large applications with extensive state updates or complex UI components, there can still be performance overhead, especially if not properly optimized.

---

## Future Improvements

1. **Asynchronous Data Processing**:

   - **Current State**: The data processing pipeline is currently run directly using a command like python pipeline.py. The pipeline executes sequentially or asynchronously as needed, but it is manually triggered from the command line. This approach works well for small to medium-sized data volumes but lacks advanced scheduling and orchestration features.
   - **Improvement**: Introduce **Celery** or **RabbitMQ** to handle more complex background processing and scheduling of the pipeline.

2. **Optimizing Sentiment Analysis**:

   - **Current State**: Sentiment analysis and issue extraction rely on calling the OpenAI API for each review.
   - **Improvement**:
     - Celery or RabbitMQ can be introduced to handle more complex background processing, task orchestration, and scheduling of the pipeline. These tools allow for better task management, retries, and monitoring. Celery can be integrated with FastAPI to provide better control over periodic or scheduled tasks, making the pipeline more scalable and resilient in production environments.
     - Additionally, cron jobs or Airflow can be used for scheduling tasks:
       - Cron Jobs: For simple, time-based scheduling of the pipeline (e.g., running once a day or weekly). This allows for periodic execution of the pipeline without the need for manual intervention.
       - Airflow: For more complex workflows, where multiple tasks need to be managed in sequence with dependencies, retries, and failure handling. Airflow enables you to orchestrate the entire pipeline, define DAGs (Directed Acyclic Graphs), and manage scheduling and retries with full visibility.

3. **Scalability**:

   - **Current State**: The pipeline works well for moderate-sized datasets (e.g., tens of thousands of reviews).
   - **Improvement**: Scale the pipeline to handle **millions of products/reviews**. This can be done by implementing **data streaming**, **distributed task queues**, and **database partitioning**.

4. **Error Handling and Monitoring**:

   - **Current State**: The backend has basic error handling, and the frontend handles some common edge cases.
   - **Improvement**: Implement **advanced error handling** and **monitoring** for better observability of the system’s health, especially for large-scale deployments.

5. **Frontend Enhancements**:

   - **Current State**: The frontend is basic, with simple product insights displayed in a list.
   - **Improvement**: Implement more sophisticated visualizations (e.g., charts, graphs) for product insights. Use libraries like **Chart.js** or **D3.js** to display sentiment trends, issues, and other metrics over time.

6. **User Authentication**:

   - **Current State**: The system does not have user authentication.
   - **Improvement**: Implement **OAuth2** or **JWT** authentication to allow different user roles (e.g., admins and regular users).

7. **Automated Data Updates**:
   - **Current State**: Data needs to be manually triggered or scheduled for periodic execution.
   - **Improvement**: Introduce a system where product data is automatically updated periodically, such as **integrating web scraping** tools or **real-time data streaming** for dynamic datasets.

---

## Prerequisites

Before running the project, ensure the following are installed:

- **Docker**: For running PostgreSQL in a container.
- **Node.js & npm**: For running the React frontend.
- **Python 3.8+**: For running the FastAPI backend.
- **PostgreSQL**: Either installed locally or running in a Docker container.

---

## Backend Setup

### 1. Create a Virtual Environment

To create a virtual environment for the backend (Python), follow these steps:

1. Navigate to the backend folder (where `requirements.txt` is located):
   ```bash
   cd /path/to/your/application
   ```
2. Create a virtual environment:

   ```
   python -m venv venv
   ```

3. Create a virtual environment:

   ```
   venv\Scripts\activate #Unix or MacOs source venv/bin/activate
   ```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DATABASE_URL=postgresql://postgres:mysecretpassword@localhost:5433/mydatabase
OPENAI_API_KEY=your_openai_api_key
```

## Frontend Setup

### 1. Navigate to Frontend Directory

```
cd frontend
npm install
```

### 2. Set Environment Variables

Create a `.env` file in the root directory with the following variables:

```
NEXT_PUBLIC_BACKEND_API=http://localhost:8000/api/v1
```

## Running the Application

### 1. Start PostgreSQL Container

```
docker-compose up -d postgres
```

### 2. Start Backend Server

From the backend directory with activated virtual environment

```
.\venv\Scripts\activate
```

```
python ./app/main.py
```

### 3. Start Frontend Development Server

From the frontend directory

```
npm run dev
```

## Docker Setup for PostgreSQL

The project uses Docker Compose to manage PostgreSQL. The configuration is defined in the docker-compose.yml file.

### 1. Start PostgreSQL Container

```
docker-compose up -d postgres
```

```
docker-compose ps
```

### 3. Access PostgreSQL

Connect to PostgreSQL using psql

```
docker exec -it <container_id> psql -U postgres -d mydatabase
```

### Database Configuration

The PostgreSQL container is configured with:

- Port: 5433 (mapped to internal 5432)
- Database: mydatabase
- Username: postgres
- Password: mysecretpassword

## Testing the API

### 1. Using Swagger UI

FastAPI automatically generates interactive API documentation. Access it at:

```
http://localhost:8000/docs
```

### 2. Using cURL

Test the products endpoint:
Get list of products

```
curl http://localhost:8000/api/v1/products
```

Get specific product insights

```
curl http://localhost:8000/api/v1/product/1

```

### 3. Running Tests

From the backend directory

```
npm run test
```

## Conclusion

You have successfully set up a FastAPI backend with a React frontend to display Amazon product insights. Docker is used for running PostgreSQL in a container to manage product data. The system provides an API for retrieving product insights and supports pagination for large datasets.

Let me know if you encounter any issues or need help with further enhancements! """
