FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# # --- Added for passing GCP credentials ---
# ARG GCP_CREDS
# COPY ${GCP_CREDS} /app/gcp-key.json
# ENV GOOGLE_APPLICATION_CREDENTIALS="/app/gcp-key.json"
# # -----------------------------------------

COPY . .

RUN pip install --no-cache-dir -e .

# RUN python pipeline/training_pipeline.py

EXPOSE 8080

#CMD ["python", "application.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "application:app"]

