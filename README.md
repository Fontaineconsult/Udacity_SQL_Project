# Udacity_SQL_Project
SQL Project

This is the SQL Logs Project for Udacity FSND.

In order to run this file you will need the following:

1. Postgresql
2. The SQL logs data file included in the vagrant machine provided by the FSND degree

In order to run the provided python file you will first need to build 4 psql views. When connected to the logs database,
run the following commands.

1. CREATE VIEW clean_path AS 
SELECT "right"(log.path, '-9'::integer) AS article_path FROM log;

2. CREATE VIEW clean_logs AS 
SELECT "right"(log.path, '-9'::integer) AS "right",
    log.ip,
    log.method,
    log.status,
    log."time",
    log.id
   FROM log;
 
 3. CREATE VIEW error_view AS
SELECT date(time) AS date,
       count(*) AS views
FROM log
WHERE status != '200 OK'
GROUP BY date(time);

4. CREATE VIEW total_view AS
SELECT date(time) AS date,
       count(*) AS views
FROM log
GROUP BY date(time);

The python file should run and you should see the following output:

The top articles are:

    1. Candidate is jerk, alleges rival - 338647 views

    2. Bears love berries, alleges bear - 253801 views

    3. Bad things gone, say good people - 170098 views


The top authors are:

    1. Ursula La Multa - 507594 views

    2. Rudolf von Treppenwitz - 423457 views

    3. Anonymous Contributor - 170098 views

    4. Markoff Chaney - 84557 views


The dates with 404 errors  greater than 1 percent  are:

     1. July 17, 2016 - 2.26%

