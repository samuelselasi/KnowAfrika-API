# Database
This directory contains details of the PostgreSQL database for the API.

## setup
Considering the installation and setup in
the [backend](../backend) directory were successful,
the [script](./db_setup.sql) can be used to set up
the schemas even though most of the routers
use ORM mode for the schemas.

## data
To save time of manually entering data, there is a [dump](./db_dump_2.sql)
available to be used with the following command:
```
pg_restore -U your_username -h your_host -d your_database < your_dump_file.sql
```
***where***:
* `your_username`: Your PostgreSQL username.
* `your_host`: The host where your PostgreSQL server is running.
Use localhost if it's on the same machine.
* `your_database`: The name of the database you want to restore.
* `your_dump_file.sql`: The name of the dump file you want to restore.

