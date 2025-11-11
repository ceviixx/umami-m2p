def data_already_setup(conn):
    try:
        cursor = conn.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")

        row_count = cursor.fetchone()[0]

        if row_count > 0:
            print(f"The table '{table_name}' contains {row_count} rows.")
        else:
            print(f"The table '{table_name}' is empty.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
