FROM apache/spark:python3

USER root

# 1. Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev python3-venv \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Fix the existing 'spark' user
RUN mkdir -p /home/spark && \
    usermod -d /home/spark -s /bin/bash spark && \
    chown -R spark:spark /home/spark

# 3. Create Venv
RUN python3 -m venv /opt/airflow_venv && \
    chown -R spark:spark /opt/airflow_venv

WORKDIR /opt/spark/work-dir

# 4. Set Airflow Home to the INTERNAL home directory (Safe from Mac permission issues)
# 4. Set Airflow Home and make it WORLD WRITABLE for the init phase
ENV AIRFLOW_HOME=/home/spark/airflow
RUN mkdir -p $AIRFLOW_HOME/logs $AIRFLOW_HOME/dags $AIRFLOW_HOME/plugins && \
    chown -R spark:spark /home/spark && \
    chmod -R 777 /home/spark/airflow  # Radical permissions to bypass the M1 kernel block

USER spark

# 5. Install Airflow
COPY requirements.txt .
RUN /opt/airflow_venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/airflow_venv/bin/pip install --no-cache-dir \
    "apache-airflow[smtp,postgres,pandas]==2.7.1" \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.7.1/constraints-3.10.txt" && \
    /opt/airflow_venv/bin/pip install --no-cache-dir pyspark streamlit

ENV PATH="/opt/airflow_venv/bin:$PATH"
ENV PYTHONPATH="/opt/spark/work-dir/src:${PYTHONPATH}"

COPY --chown=spark:spark . .