
# Umami MySQL to PostgreSQL Migration Tool


> [!CAUTION]
> Tested on version 2.18.1 - Please verify all your sources and data.

This tool enables the migration of [Umami](https://github.com/umami-software/umami) data from an existing **MySQL database** to a new, **empty PostgreSQL database**.

⚠️ **Important Notice:**  
The target PostgreSQL database **must not be initialized** by Umami beforehand. All necessary tables will be created automatically during the migration.  
It is strongly recommended to perform the migration **on a staging database first** to verify the result before using it in production.

---

## ✅ Features

- Extracts all Umami data from MySQL
- Automatically creates the database schema in PostgreSQL
- Transfers data consistently and completely
- Configurable via `.env` file
- After a successful migration, Umami can be started directly using the PostgreSQL database

---

## 🔧 Requirements

- Python 3.8+
- An empty PostgreSQL database (not initialized by Umami)
- Access to the existing MySQL database containing Umami data

---

## 🚀 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ceviixx/umami-m2p.git
   cd umami-m2p
   ```

2. Install the Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Create and configure your `.env` file:

   ```env
   # MySQL connection parameters
   MYSQL_HOST=
   MYSQL_DATABASE=
   MYSQL_USER=
   MYSQL_PASSWORD=
   MYSQL_PORT=3306

   # PostgreSQL connection parameters
   POSTGRES_HOST=
   POSTGRES_DATABASE=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_PORT=5432
   ```

---

## ▶️ Usage

```bash
python3 migrate.py
```

The script will export data from MySQL and then transfer it to the PostgreSQL database.

---

## 🛑 Important Notes
- The PostgreSQL database **must be empty**.
- Umami **must not have been initialized** in the target PostgreSQL database.
- Always test the migration on a **staging database** first.
- After migration, Umami can be started immediately using the new PostgreSQL database.
