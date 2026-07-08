# Stage 1: builder — εδώ κάνουμε το pip install
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt /app

RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: runtime — καθαρό, μόνο ό,τι χρειάζεται να τρέξει
FROM python:3.12-slim

WORKDIR /app

# Παίρνουμε ΜΟΝΟ τα installed packages από το builder
COPY --from=builder /root/.local /root/.local

COPY . /app

# Βεβαιώσου ότι το Python βρίσκει τα --user installed packages
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD [ "python","app.py"]