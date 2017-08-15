#!/usr/bin/env python
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
    items_string = ""
    n = 1
    for a,b in returned_data:
        output_string = "    {item}. {name} - {count} views \n \n".format(item = n, name = a, count = b)
        items_string = items_string + output_string
        n+=1


    return("The top articles are:\n \n {output_list}".format(output_list=items_string))


def find_top_authors():

    cursor = database.cursor()
    cursor.execute(
        "SELECT authors.name, count(authors.name) "
        "FROM authors INNER JOIN articles ON authors.id = articles.author "
        " INNER JOIN clean_logs ON articles.slug = clean_logs.right "
        " GROUP BY authors.name ORDER BY count(authors.name) DESC;"
        )
    returned_data = cursor.fetchall()
    items_string = ""
    n = 1
    for a,b in returned_data:
    	output_string = "    {item}. {name} - {count} views \n \n".format(item = n, name = a, count = b)
    	items_string = items_string + output_string
    	n+=1


    return("The top authors are:\n \n {output_list}".format(output_list=items_string))

  


def find_top_error():

    cursor = database.cursor()
    cursor.execute(
        '''
        SELECT to_char(total_view.date, 'FMMonth FMDD, YYYY') as date,
            round(100 * error_view.views / total_view.views::decimal, 2) as views
        FROM error_view
        JOIN total_view on error_view.date = total_view.date
        WHERE error_view.views / total_view.views::decimal > 0.01
        ORDER BY error_view.views / total_view.views::decimal desc;
        '''
        )
  
    returned_data = cursor.fetchall()
    
    items_string = ""
    n = 1
    for a,b in returned_data:
        output_string = "    {item}. {name} - {count}% \n \n".format(item = n, name = a, count = b)
        items_string = items_string + output_string
        n+=1
    
    return("The dates with 404 errors greater than 1 percent are:\n \n {output_list}".format(output_list=items_string))


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
