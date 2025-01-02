# Gebruik een officiële Python-basisafbeelding
FROM python:3.11-slim

# Stel de werkdirectory in
WORKDIR /app

# Kopieer alleen requirements.txt en installeer afhankelijkheden
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de rest van de applicatie
COPY . .

# Stel het standaard startcommando in
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000"]

