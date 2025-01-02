# Gebruik een lichtgewicht Python-image
FROM python:3.13.1

# Stel de werkdirectory in
WORKDIR /app

# Kopieer alle bestanden naar de container
COPY . .

# Start het Python-script
CMD ["python", "main.py"]

