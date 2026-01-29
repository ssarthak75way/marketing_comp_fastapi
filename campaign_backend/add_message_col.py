import psycopg2
from app.core.config import DATABASE_URL

def add_message_column():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        conn.autocommit = True
        
        print("Adding 'message' column to 'campaigns' table...")
        try:
            cur.execute("ALTER TABLE campaigns ADD COLUMN message VARCHAR")
            print("'message' column added successfully.")
        except psycopg2.errors.DuplicateColumn:
            print("'message' column already exists.")
        
        cur.close()
    except Exception as e:
        print(f"Error adding column: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_message_column()
