import json
import boto3
import psycopg2
import pandas as pd
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # ---- Load JSON from S3 ----
        bucket = 'azyryano-earthquake-pipeline'
        key = 'earthquake-data-2025-07-26T03-02-33Z.json'
        obj = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(obj['Body'].read())

        # ---- Parse JSON ----
        features = data.get('features', [])
        rows = []
        for f in features[:500]:  # Limit to 500 rows for testing
            props = f['properties']
            rows.append({
                'id': f['id'],
                'place': props.get('place'),
                'magnitude': props.get('mag'),
                'time': int(props.get('time')) if props.get('time') else None
            })

        df = pd.DataFrame(rows)

        # ---- Write CSV to memory ----
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False, header=False)
        csv_buffer.seek(0)

        # ---- Connect to RDS ----
        conn = psycopg2.connect(
            host="database-azyryano.cfkcqqqsm3g5.us-east-2.rds.amazonaws.com",
            database="databaseazyryano",
            user="postgres",
            password="Your password",  # Replace securely
            port=5432
        )
        cur = conn.cursor()

        # ---- Use COPY for fast insert ----
        copy_sql = """
            COPY earthquakes (id, place, magnitude, time)
            FROM STDIN WITH CSV;
        """
        cur.copy_expert(sql=copy_sql, file=csv_buffer)
        conn.commit()

        cur.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": f"{len(df)} earthquake records uploaded using COPY"
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
