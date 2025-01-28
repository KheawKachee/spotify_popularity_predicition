# Base image
FROM apache/airflow:2.7.0

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-jdk curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Download and install Spark
RUN curl https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.4-bin-without-hadoop.tgz -o /tmp/spark-3.5.4-bin-without-hadoop.tgz && \
    mkdir -p /opt/spark && \
    tar -xvzf /tmp/spark-3.5.4-bin-without-hadoop.tgz --directory /opt/spark --strip-components=1 && \
    rm /tmp/spark-3.5.4-bin-without-hadoop.tgz

# Set environment variables
ENV JAVA_HOME='/usr/lib/jvm/java-17-openjdk-amd64'
ENV PATH=$PATH:$JAVA_HOME/bin
ENV SPARK_HOME='/opt/spark'
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Copy project files
COPY . .

# Optional: Set entrypoint or default command
#CMD ["python", "etl.py"]
