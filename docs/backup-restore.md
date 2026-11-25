# Backup and restore

Run the Windows backup script from the project directory while Docker is running:

```powershell
.\scripts\backup.ps1
```

It exports PostgreSQL and archives uploaded CV files under `backups/`. That directory is ignored by Git.

To restore PostgreSQL, start the database and pipe a dump into it:

```powershell
docker compose up -d db
Get-Content .\backups\careermatch-YYYYMMDD-HHMMSS.sql | docker compose exec -T db psql -U careermatch -d careermatch
```

Restore uploaded files by extracting the matching archive into `uploads/`. Keep backups on separate protected storage in production and test restores periodically.

