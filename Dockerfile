# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app
RUN pip install --upgrade pip setuptools wheel

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy only the necessary code into the container
COPY exec_analysis.py /exec_analysis.py

# Define a volume for storing data outside the container
VOLUME /app/data

# Set the environment variable to point to the external volume
ENV DATA_DIR /app/data

CMD ["python", "exec_analysis.py"]