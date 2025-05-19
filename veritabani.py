import psycopg2

def baglanti_kur():
    try:
        conn= psycopg2.connect(
            dbname= "diabetes-following-system",
            user= "postgres",
            password= "merve813",
            host= "localhost",
            port= "5432"
        )
        return conn
    except Exception as e:
        print(f"Veritabanı Bağlantı Hatası: {e}")
        return None
