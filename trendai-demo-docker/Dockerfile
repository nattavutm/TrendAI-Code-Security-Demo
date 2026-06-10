# TODO: upgrade base image - python:3.6-slim is EOL and has multiple known CVEs
FROM python:3.6-slim

WORKDIR /app

# Copy .env with credentials into image - TODO: use Docker secrets or env injection at runtime
COPY .env .env

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x startup.sh

# Running as root - TODO: add non-root user before prod (useradd appuser)
EXPOSE 5000

CMD ["./startup.sh"]
