
# Umami MySQL to PostgreSQL Migration Tool

Migrate your [Umami Analytics](https://github.com/umami-software/umami) installation from **MySQL** to **PostgreSQL** with ease.

[![Test Migration](https://github.com/ceviixx/umami-m2p/actions/workflows/test-migration.yml/badge.svg)](https://github.com/ceviixx/umami-m2p/actions/workflows/test-migration.yml)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Migration](https://img.shields.io/badge/Migration-MySQL→PostgreSQL-green)
![Umami](https://img.shields.io/badge/Umami-mysql--latest-orange)
![Tested](https://img.shields.io/badge/Tested%20with-Umami%202.18.1-success)

> [!CAUTION]  
> **Important Safety Information**
> - Provided as-is **without any warranty**
> - **Always create a backup** of your MySQL database before starting
> - **Test thoroughly in a staging environment** before production use
> - The author assumes no responsibility for data loss or corruption


---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed
- **Source database**: A MySQL database with existing Umami data
- **Target database**: An empty PostgreSQL database (**not initialized by Umami**)
- Network access to both databases

> [!WARNING]  
> The PostgreSQL database **must be completely empty**. The migration script will create all necessary tables and indexes automatically.

---

## ✨ Features

- 🔄 **Complete data migration** - Transfers all Umami tables and data
- 🏗️ **Automatic schema creation** - Creates PostgreSQL schema with proper indexes
- ✅ **Data integrity** - Maintains referential integrity and constraints
- ⚙️ **Easy configuration** - Simple `.env` file setup
- 🚀 **Production ready** - Use PostgreSQL database immediately after migration

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/ceviixx/umami-m2p.git
cd umami-m2p
```

### 2. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 3. Configure database connections

Copy the example environment file and edit it with your database credentials:

```bash
cp .env.example .env
# Then edit .env with your MySQL and PostgreSQL connection details
```

### 4. Run the migration
```bash
python3 migrate.py
```

The script will:
1. ✓ Verify database connections
2. ✓ Check that PostgreSQL database is empty
3. ✓ Create all necessary tables and indexes
4. ✓ Migrate data from MySQL to PostgreSQL
5. ✓ Verify data integrity

---

## 📊 What Gets Migrated

The tool migrates all Umami tables including:

- `user` - User accounts and credentials
- `team` - Team information
- `team_user` - Team memberships
- `website` - Website configurations
- `session` - Visitor sessions
- `website_event` - Page views and events
- `event_data` - Custom event data
- `session_data` - Session-specific data
- `report` - Saved reports
- `revenue` - Revenue tracking data
- `segment` - User segments and targeting
- `_prisma_migrations` - Migration history

---

## ⚠️ Important Notes

- **Backup first!** Always create a complete backup of your MySQL database
- **Empty target required**: The PostgreSQL database must not contain any Umami tables
- **Test first**: Run the migration on a staging environment before production
- **Downtime**: Plan for downtime during migration as Umami should not write to MySQL during the process
- **Connection**: Ensure both databases are accessible from where you run the script

---

## 🐛 Troubleshooting

### Connection Issues
- Verify database credentials in `.env` file
- Check that both databases are running and accessible
- Ensure firewall/security groups allow connections

### Migration Fails
- Confirm PostgreSQL database is completely empty
- Check that MySQL database contains Umami data
- Review console output for specific error messages

### After Migration
- Update your Umami configuration to use the PostgreSQL connection string
- Test Umami functionality thoroughly before going live
- Keep your MySQL backup until you're confident everything works

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/ceviixx/umami-m2p/issues).

---

## ⭐ Support

If this tool helped you migrate your Umami instance, consider giving it a star on GitHub!
