# Udacity_SQL_Project
SQL Project

This is the SQL Logs Project for Udacity FSND.

The purpose of this project is develop basic SQL skills by developing a variety of queries using SQL that ask the following three questions of website log database.

1.What are the most popular three articles of all time?
2.Who are the most popular article authors of all time?
3.On which days did more than 1% of requests lead to errors?

In order to run this file you will need the following:

1. Python 2 or 3
2. A linux environment with Postgresql and psychopg2 for python
3. The SQL logs data file included in the vagrant machine provided by the FSND degree


To begin, CD to the location of the provided SQL file and run the following command. 

1. psql -d news -f newsdata.sql.

This will initialize the PSQL database with the logs data.

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

Thank you.
