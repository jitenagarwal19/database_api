from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.db import connection
import simplejson as json

# Create your views here.
def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print r.text
    return HttpResponse('<pre>' + r.text + '</pre>')


def perform_database_operations(request):
    result = 'smooth'
    return HttpResponse('hey there in the perform database operations  ' + result)


def create_new_table(request):
    with connection.cursor() as cursor:
        cursor.execute('create table temp1(hello int)')

    return HttpResponse('table created without any errors I guess')



def insert_something(request, something):

    with connection.cursor() as cursor:
        cursor.execute('insert into temp1 values (%s)', [something])

    return HttpResponse('hey there we have successfully inserted something ' + something)

def get_count_of_temp1(request):
    with connection.cursor() as cursor:
        cursor.execute('select count(*) from temp1')
        rows = cursor.fetchone()
        rows = str(rows[0])

    return HttpResponse('hey there count of table temp1 = ' + rows)

def get_content_of_temp1(request):

    with connection.cursor() as cursor:
        cursor.execute('select * from temp1');
        rows = cursor.fetchall()
        result = [];
        i = 0;
        for row in rows:
            i= i + 1
            tempObj = {'hmmm':i, 'value':row[0]}
            # print('at ' + i + '   ' + te)
            result.append(json.dumps(tempObj))

    return HttpResponse('content of temp1 <br \>' + json.dumps(result))



