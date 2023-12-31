# Use the official Python image with tag 3.11.7
FROM python:3.11.7

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY main.py /app

CMD ["python", "main.py"]