# Database

## Content
* [About](#about)
* [Setup](#setup)
* [Dumps](#dumps)
* [Scripts](#scripts)
* [RawData](#rawdata)
* [Tables](#tables)
* [Files](#files)

## About
This directory contains database details from
scripts to current dumps.

## Setup
Considering the installation and setup in
the [backend](../backend) directory were successful,
the [script](./db_setup.sql) can be used to set up
the schemas even though most of the routers
use ORM mode for the schemas.

## [Dumps](./dumps)
To save time of manually entering data, there is a [dump](./dumps/db_dump_3.sql)
available to be used with the following command:
```
pg_restore -U your_username -h your_host -d your_database < your_dump_file.sql
```
where:
* `your_username`: Your PostgreSQL username.
* `your_host`: The host where your PostgreSQL server is running.
Use localhost if it's on the same machine.
* `your_database`: The name of the database you want to restore.
* `your_dump_file.sql`: The name of the dump file you want to restore.


## [Scripts](./scripts)
This directory contains two types of scrips:
- Scripts to scrape raw data
- Scripts to setup database

## [Raw Data](./raw_data)
This directory contains raw data to be processed and trasfered to the database


## [Tables](./tables)
This directory contains sql scripts to create tables


## Files

- `db_setup.sql` -> script tocreate entire db infrastructure
- `knowafrika.png` -> ERD of tables in the database
