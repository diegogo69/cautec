# Connection URL Format

A basic database connection URL uses the following format. Username, password, host, and port are optional depending on the database type and configuration.

`dialect://username:password@host:port/database`

Here are some example connection strings:

## SQLite, relative to Flask instance path

`sqlite:///project.db`

## MySQL / MariaDB

MySQL default port is 3306

`mysql://scott:tiger@localhost/project`

## PostgreSQL

`postgresql://scott:tiger@localhost/project`

SQLite does not use a user or host, so its URLs always start with _three_ slashes instead of two. The dbname value is a file path. Absolute paths start with a _fourth_ slash (on Linux or Mac). Relative paths are relative to the Flask application’s instance_path.