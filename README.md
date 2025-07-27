# Earthquake ETL Pipeline (S3 to RDS PostgreSQL)

This project demonstrates a serverless ETL pipeline that extracts earthquake data from the USGS Earthquake API, stores it in Amazon S3 (raw zone), and loads it into an AWS RDS PostgreSQL database for downstream analytics.

## 📦 Project Structure

```
earthquake-etl/
│
├── etl_postgres_upload.py        # Jupyter-compatible script to load data from S3 to RDS PostgreSQL
├── requirements.txt              # Python package dependencies
└── README.md                     # Project overview and instructions
```

## ⚙️ Tech Stack

- **Data Source**: USGS Earthquake GeoJSON API
- **Ingestion**: AWS Lambda (raw) → Amazon S3
- **Transformation & Load**: Python (Jupyter) → AWS RDS PostgreSQL
- **Storage Zones**: 
  - `raw/`: Raw GeoJSON files
  - `processed/`: (Future) Cleaned & transformed files

## 🗃️ Database Schema

```sql
CREATE TABLE earthquakes (
  id TEXT PRIMARY KEY,
  place TEXT,
  magnitude NUMERIC,
  time BIGINT
);
```

## 🚀 How to Run

1. Upload a GeoJSON file to S3 under the `raw/` prefix.
2. In Jupyter, run `etl_postgres_upload.py` with the correct file key.
3. Verify the data in your PostgreSQL instance.

## 🧠 Lessons Learned

- **Lambda Timeout**: COPY operations or large inserts can exceed Lambda’s timeout limit.
- **Better with COPY**: `psycopg2.copy_expert` is significantly faster than `executemany()`.
- **IAM & VPC**: Lambda to RDS requires VPC access and EC2 permissions.
- **Testing in Jupyter**: Easier debugging, no timeout limits, better visibility.

## 📌 Next Steps

- Add deduplication logic (e.g., `ON CONFLICT DO NOTHING` fallback).
- Build a Glue/Athena pipeline for querying at scale.
- Add CloudWatch logging and failure notifications.
