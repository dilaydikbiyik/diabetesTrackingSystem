import psycopg2

def baglanti_kur():
    try:
        conn = psycopg2.connect(
            dbname="diabetes_tracking_system",
            user="postgres",
            password="veritabani13",
            host="localhost",
            port="5432",
            options='-c search_path=public'
        )
        with conn.cursor() as cur:
            cur.execute("SET TIME ZONE 'Europe/Istanbul';")
        return conn
    except Exception as e:
        print(f"Veritabanı Bağlantı Hatası: {e}")
        return None
