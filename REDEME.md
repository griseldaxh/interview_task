# Steps to Run the Project

## 1. Set Up PostgreSQL with Docker

If you're using Docker for PostgreSQL, you need to follow these steps first.

### 1.1. Install Docker

- **Windows/macOS**: Download Docker Desktop from Docker's official website and install it.
- **Linux**: Install Docker using your package manager (e.g., `apt-get install docker.io` for Ubuntu).
- Once installed, open Docker and make sure it's running.

### 1.2. Pull PostgreSQL Docker Image

Pull the latest PostgreSQL image from Docker Hub:

docker pull postgres

1.3. Run PostgreSQL in Docker
Start the PostgreSQL container with the following command:

```bash
docker run --name SellerX -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres
```

This command will create a container named `postgres-container` with the password `mysecretpassword` and the database `mydatabase`.

To verify the container is running:

```bash
docker ps
```

### 1.4. (Optional) Connect to PostgreSQL

To connect to your PostgreSQL instance and verify it:

```
psql -h localhost -U postgres -d mydatabase
```

## 2. Set Up Your Python Environment

### 2.1. Install Python 3.8+ and Set Up Virtual Environment

Make sure Python 3.8 or higher is installed on your machine. You can verify this by running:

```
python --version
```
