# FROM zauberzeug/nicegui
FROM python:3.12-slim

WORKDIR /app

# Copy your requirements.txt file and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=8080

# Copy the rest of your app's source code
COPY . /app

RUN useradd -m myuser
USER myuser


CMD ["python", "main.py"]