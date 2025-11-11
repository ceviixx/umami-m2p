def data_already_setup(conn):
    try:
        cursor = conn.cursor()

        # SQL query to count the number of rows in the table
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")

        # Get the result of the query
        row_count = cursor.fetchone()[0]

        # Check if the table contains data
        if row_count > 0:
            print(f"The table '{table_name}' contains {row_count} rows.")
        else:
            print(f"The table '{table_name}' is empty.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()
