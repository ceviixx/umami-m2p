def data_already_setup(conn):
    try:
        cursor = conn.cursor()

        # SQL-Abfrage, um die Anzahl der Zeilen in der Tabelle zu zählen
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")

        # Ergebnis der Abfrage holen
        row_count = cursor.fetchone()[0]

        # Prüfen, ob die Tabelle Daten enthält
        if row_count > 0:
            print(f"Die Tabelle '{table_name}' enthält {row_count} Zeilen.")
        else:
            print(f"Die Tabelle '{table_name}' ist leer.")

    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        # Cursor und Verbindung schließen
        cursor.close()
        conn.close()
