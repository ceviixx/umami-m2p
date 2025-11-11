def fetch_data(cur, table_name):
    cur.execute(f"SELECT * FROM {table_name};")
    rows = cur.fetchall()
    
    if not rows:
        return []
    else:
        return rows