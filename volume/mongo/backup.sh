#!/bin/bash

set -e

DB=one
BACKUP_NAME=$(date +%y%m%d_%H%M%S).gz
USERNAME=one
PASSWORD=123qwe

date
echo "Backing up MongoDB databas"

echo "Dumping MongoDB $DB database to compressed archive"

mongodump --db $DB --username $USERNAME --password $PASSWORD --archive=$HOME/backup/$BACKUP_NAME --gzip

echo "Backup complete!"
