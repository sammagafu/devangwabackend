#!/bin/bash
# Database backup script
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/app/backups
mkdir -p $BACKUP_DIR

if [ "$DATABASE_ENGINE" = "django.db.backends.postgresql" ]; then
    pg_dump -h $DATABASE_HOST -U $DATABASE_USER -d $DATABASE_NAME > $BACKUP_DIR/backup_$DATE.sql
elif [ "$DATABASE_ENGINE" = "django.db.backends.sqlite3" ]; then
    cp /app/devangwabackend/db.sqlite3 $BACKUP_DIR/backup_$DATE.sqlite3
fi

# Keep only last 7 backups
cd $BACKUP_DIR
ls -t | tail -n +8 | xargs rm -f