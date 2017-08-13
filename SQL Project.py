import psycopg2


database = psycopg2.connect("dbname=news")


def find_top_articles():

    cursor = database.cursor()
    cursor.execute(
        "SELECT articles.title, count(clean_path.article_path) "
        "FROM articles "
        "INNER JOIN clean_path ON (articles.slug = clean_path.article_path) "
        "GROUP BY articles.title ORDER BY count(clean_path.article_path) "
        "DESC LIMIT 3"
        )
    returned_data = cursor.fetchall()
    start_string = '''
    \n The top three articles are: \n \n
        1. {x[0][0]} - {x[0][1]} views \n
        2. {x[1][0]} - {x[1][1]} views \n
        3. {x[2][0]} - {x[2][1]} views \n
    '''
    return (start_string.format(x=returned_data))


def find_top_authors():

    cursor = database.cursor()
    cursor.execute(
        "SELECT authors.name, count(authors.name) "
        "FROM authors INNER JOIN articles ON authors.id = articles.author "
        " INNER JOIN clean_logs ON articles.slug = clean_logs.right "
        " GROUP BY authors.name ORDER BY count(authors.name) DESC LIMIT 3;"
        )
    returned_data = cursor.fetchall()
    start_string = '''
    \n The top three authors are: \n \n
        1. {x[0][0]} - {x[0][1]} views \n
        2. {x[1][0]} - {x[1][1]} views \n
        3. {x[2][0]} - {x[2][1]} views \n
    '''
    return (start_string.format(x=returned_data))


def find_top_error():

    cursor = database.cursor()
    cursor.execute(
        '''
        SELECT to_char(date, 'FMMonth DD, YYYY'), "200 OK", "400 Not Found",
        "400 Not Found"::decimal / "200 OK"::decimal as "Error Percent"
        FROM crosstab_errors
        WHERE "400 Not Found"::decimal / "200 OK"::decimal > 0.01
        '''
        )
    returned_data = cursor.fetchall()
    date = returned_data[0][0]
    error_rate = "{:.1%}".format(returned_data[0][3])
    start_string = '''
    \n The date with '404 Not Found' errors greater than 1% is \n \n
        * {date} - {error}. \n \n
    '''
    return(start_string.format(date=date, error=error_rate))


print (find_top_articles())
print (find_top_authors())
print (find_top_error())


"""
clean_path =  SELECT "right"(log.path, '-9'::integer) AS article_path FROM log;

 clean_logs =  SELECT "right"(log.path, '-9'::integer) AS "right",
    log.ip,
    log.method,
    log.status,
    log."time",
    log.id
   FROM log;

top_3 = SELECT articles.title, (count)clean_path.article_path AS count
FROM articles JOIN clean_path on articles.slug = clean_path.article_path
GROUP BY articles.title
ORDER BY (count(clean_path.article_path)) DESC;

Authors Join:
SELECT authors.name, articles.title, clean_logs.right
FROM authors
INNER JOIN articles ON authors.id = articles.author
INNER JOIN clean_logs ON articles.slug = clean_logs.right;

errors view:
SELECT date(time), status, count(date(time))
FROM log group by date(time), status
ORDER BY date(time) desc;

crosstab_errors view:
SELECT * FROM crosstab( 'select date, status, count
FROM errors ORDER BY 1,2;' )
as final_result(date date, "200 OK" BIGINT, "400 Not Found" BIGINT);
"""
