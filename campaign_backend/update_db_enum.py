import psycopg2
from app.core.config import DATABASE_URL

def update_enum():
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Check current values in the enum (optional but safer)
        # However, ADD VALUE IF NOT EXISTS is not standard in old PG, 
        # but in modern PG (9.1+) we can use ALTER TYPE ... ADD VALUE ...
        
        print("Updating campaignfrequency enum...")
        
        # Note: ALTER TYPE ADD VALUE cannot run inside a transaction block in some PG versions
        # so we set autocommit to True
        conn.autocommit = True
        
        frequencies = ['secondly', 'hourly'] # new table insert
        
        for freq in frequencies:
            try:
                cur.execute(f"ALTER TYPE campaignfrequency ADD VALUE '{freq}'")
                print(f"Added '{freq}' to campaignfrequency enum.")
            except psycopg2.errors.DuplicateObject:
                print(f"'{freq}' already exists in campaignfrequency enum.")
            except Exception as e:
                print(f"Could not add '{freq}': {e}")

        cur.close()
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    update_enum()
