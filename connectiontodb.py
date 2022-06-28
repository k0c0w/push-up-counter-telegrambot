import sqlite3

if __name__ == "__main__":
    try:
        conn = sqlite3.connect("database.db", check_same_thread=False)
        conn.execute("pragma journal_mode=wal;")
        curs = conn.cursor()
        while True:
            command = input()
            if command == "break":
                break;
            try:
                curs.execute("BEGIN TRANSACTION")
                curs.execute(command)
                conn.commit()
                print("успех")
            except sqlite3.Error:
                if conn:
                    conn.rollback()
                    print("откат")
    finally:
        if conn:
            conn.close()
