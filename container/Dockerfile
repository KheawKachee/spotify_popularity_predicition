# Base image
FROM apache/airflow:2.7.0
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential default-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


# Copy project files
COPY . .

#download spark
RUN curl https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.4-bin-without-hadoop.tgz -o spark-3.5.4-bin-without-hadoop.tgz

# Change permissions of the downloaded tarball
RUN chmod 755 spark-3.5.1-bin-hadoop3.tgz

# Create the target directory and extract the tarball to it
RUN mkdir -p /opt/spark && tar xvzf spark-3.5.1-bin-hadoop3.tgz --directory /opt/spark --strip-components=1

ENV JAVA_HOME='/usr/lib/jvm/java-17-openjdk-amd64'
ENV PATH=$PATH:$JAVA_HOME/bin
ENV SPARK_HOME='/opt/spark'
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin



# Default command
#CMD ["python", "etl.py"]


