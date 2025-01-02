# Gebruik een lichtgewicht Python-image
FROM python:3.10-slim

# Stel de werkdirectory in
WORKDIR /app

# Kopieer alle bestanden naar de container
COPY . .

# Start het Python-script
CMD ["python", "app.py"]

