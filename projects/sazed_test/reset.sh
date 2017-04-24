#!/bin/bash

mkdir -p ../../databases/
rm ../../databases/sazed_test.sqlite3

sqlite3 -echo ../../databases/sazed_test.sqlite3 "PRAGMA main.auto_vacuum = FULL;"  > /dev/null
sqlite3 -echo ../../databases/sazed_test.sqlite3 "PRAGMA automatic_index = 1;"      > /dev/null
sqlite3 -echo ../../databases/sazed_test.sqlite3 "PRAGMA checkpoint_fullfsync = 1;" > /dev/null
sqlite3 -echo ../../databases/sazed_test.sqlite3 "PRAGMA fullfsync = 1;"            > /dev/null
sqlite3 -echo ../../databases/sazed_test.sqlite3 "PRAGMA main.journal_mode = WAL;"  > /dev/null
sqlite3 -echo ../../databases/sazed_test.sqlite3 "PRAGMA main.schema_version = 0;"  > /dev/null
sqlite3 -echo ../../databases/sazed_test.sqlite3 "PRAGMA main.user_version = 0;"    > /dev/null
sqlite3 -echo ../../databases/sazed_test.sqlite3 "PRAGMA main.synchronous = EXTRA;" > /dev/null

./manage.py migrate --run-syncdb
#./manage.py createsuperuser --username admin --noinput --email admin@local
#./manage.py changepassword admin

echo "==== TABLES ===="
# type|name|tbl_name|rootpage|sql
sqlite3 ../../databases/sazed_test.sqlite3 "SELECT tbl_name FROM sqlite_master WHERE type = 'table';" | sort
echo "================"

exit
