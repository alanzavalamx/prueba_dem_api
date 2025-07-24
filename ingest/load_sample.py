import csv
import os
import psycopg2
from psycopg2.extras import execute_values

# Parámetros de conexión (pueden venir de env vars)
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")


def load_csv_to_db(csv_path):
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT,
        dbname=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [
            (
                row['first_name'], row['last_name'], row.get('company_name'),
                row.get('address'), row.get('city'), row.get('state'),
                row.get('zip'), row.get('phone1'), row.get('phone2'),
                row.get('email'), row.get('department')
            )
            for row in reader
        ]

    sql = """
    INSERT INTO sample_data (
        first_name, last_name, company_name, address, city,
        state, zip, phone1, phone2, email, department
    ) VALUES %s
    ON CONFLICT DO NOTHING;
    """
    execute_values(cur, sql, rows)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    csv_file = os.path.join(os.path.dirname(__file__), "../data/sample.csv")
    load_csv_to_db(csv_file)
    print("Carga completada.")
