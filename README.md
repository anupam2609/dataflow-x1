```markdown
# Dataflow-X1: Spark + Airflow + Streamlit Platform

A containerized data engineering platform designed to run seamlessly on both M1 Mac (ARM64) and Windows/Linux (x86_64). This project orchestrates Apache Spark jobs using Airflow and visualizes data results via Streamlit.

## 🚀 Quick Start (Deployment)

Follow these steps to deploy the full stack on a new machine:

```zsh
# 1. Clone the repository
git clone [https://github.com/YOUR_USERNAME/dataflow-x1.git](https://github.com/YOUR_USERNAME/dataflow-x1.git)
cd dataflow-x1

# 2. Build the images (Detects local architecture: ARM vs AMD)
docker compose build --no-cache

# 3. Start the Database first
docker compose up -d postgres

# 4. Initialize Airflow Database and Admin User
# Note: It may exit with Code 1 on M1 Macs; this is expected.
docker compose up airflow-init

# 5. Launch all services
docker compose up -d

```

---

## 🛠️ Service Access

| Service | URL | Credentials |
| --- | -- | --- |
| **Airflow Webserver** | [http://localhost:8080](https://www.google.com/search?q=http://localhost:8080) | `admin` / `admin` |
| **Streamlit Dashboard** | [http://localhost:8501](https://www.google.com/search?q=http://localhost:8501) | N/A |
| **Postgres DB** | `localhost:5432` | `airflow` / `airflow` |


---

## 📂 Project Structure

* `/dags`: Place your Airflow DAG files here (syncs to `/home/spark/airflow/dags`).
* `/src`: Core Python logic and Spark processing scripts.
* `/ui`: Streamlit application files.
* `Dockerfile`: Multi-stage build based on `apache/spark:python3`.
* `requirements.txt`: Python dependencies (Airflow 2.7.1, PySpark, Streamlit).

---

## 💡 Key Maintenance Commands

* **Stop Services:** `docker compose down` (keeps data safe).
* **Hard Reset:** `docker compose down -v` (removes all database data/users).
* **View Logs:** `docker compose logs -f airflow-webserver`
* **Postgres:** `the postgres server is mapped to 5433 localhost port from container port 5432` (this helps connect system servers to airflow db running on docker container. Please use credentials provided in docker-compose.yml)

```

---

### Tips for the "First Move" to Windows
When you first run these commands on your Windows server:
1. **Line Endings:** If `airflow-init` fails with a "command not found" error, ensure your files are saved with **LF** line endings (VS Code status bar).
2. **Terminal:** Use **PowerShell** or **Git Bash** for the best experience with these commands on Windows.



### What would you like to build next?
Now that the project is documented and ready for Git, would you like me to help you create your **first Spark processing script** in the `/src` folder to verify the data flow?

```
