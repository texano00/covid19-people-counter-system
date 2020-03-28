#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE data.people (
        count float8 NULL,
        "date" timestamp NULL,
        code varchar(100) NULL,
        description varchar(500) NULL
    );
EOSQL

