# Base image
FROM apache/airflow:2.7.0

USER root

# Create directory for apt lists
RUN mkdir -p /var/lib/apt/lists/partial && \
    chmod 755 /var/lib/apt/lists/partial

# Install system dependencies
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-jdk \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories with proper permissions
RUN mkdir -p /opt/spark && \
    chown -R airflow:root /opt/spark && \
    chmod -R 755 /opt/spark

# Switch to airflow user for pip installations
USER airflow

# Copy requirements and install Python dependencies
COPY --chown=airflow:root requirements.txt /opt/airflow/
WORKDIR /opt/airflow
RUN pip install --no-cache-dir -r requirements.txt

# Switch back to root for Spark installation
USER root

# Download and install Spark
RUN curl -L https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-without-hadoop.tgz -o /tmp/spark.tgz && \
    tar -xf /tmp/spark.tgz -C /opt/spark --strip-components=1 && \
    rm /tmp/spark.tgz && \
    chown -R airflow:root /opt/spark

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-default \
    SPARK_HOME=/opt/spark \
    PATH="${PATH}:/usr/lib/jvm/java-default/bin:/opt/spark/bin:/opt/spark/sbin"

# Create and set working directory
RUN mkdir -p /app && \
    chown -R airflow:root /app
WORKDIR /app

# Copy project files
COPY --chown=airflow:root . .

# Switch back to airflow user for security
USER airflow