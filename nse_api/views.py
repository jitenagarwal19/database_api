from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.db import connection
import simplejson as json
import pandas as pd
import os
import datetime
import time
import math
# import numpy

# Create your views here.
_NSE ='NSE/'

def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print r.text
    return HttpResponse('<h1>Fuck THis worked</h1><pre>' + r.text + '</pre>')

def read_me_the_shit(request):
    df = pd.read_csv('nse_indices/NSIL.csv')
    return HttpResponse(str(df.head()))

def create_table_to_store_indices(request):

    with connection.cursor() as cursor:

        cursor.execute('create table if not exists indices1(id serial primary key, name varchar(30) not null, description varchar(100)) ')
        cursor.execute('select count(*) from indices1')
        row  = cursor.fetchone()
        if (row):
            result = 'count of new table ' + str(row[0])

    return HttpResponse('Table created successfully and ' + result)


def store_value_in_table(request):
    df = pd.read_csv('csv_files/data_codes.csv', header=None)
    result = ''
    with connection.cursor() as cursor:
        for i in range(0, len(df)):
            cursor.execute('insert into indices1(name, description) values(%s, %s)', df.iloc[i].tolist())

        cursor.execute('select count(*) from indices1')
        row  = cursor.fetchone()
        result = 'count of row after operation ' + str(row[0])
    return HttpResponse(result)


def get_contents_indices(request):
    with connection.cursor() as cursor:
        cursor.execute('select * from indices1')
        rows = cursor.fetchall()
        result = ''
        for row in rows:
            result += str(row) + '<br />'
    return HttpResponse(result)
def is_index_present(request, index):
    index = 'NSE/'+index.upper()
    result = ''
    with connection.cursor() as cursor:
        cursor.execute('select * from indices1 where name=%s', [index])
        row = cursor.fetchone()
        if row:
            result += str(row)
        else:
            result = 'nothing of that sort fucker ' + index
    return HttpResponse('-------'+ result)
def get_id_of_index(index):
    with connection.cursor() as cursor:
        cursor.execute('select * from indices1 where name=%s', [index])
        row = cursor.fetchone()
        if row:
            return str(row[0])
def read_data_from_local(request):
    result = ''
    print('i am here fucker')
    for roots, dirs, files in os.walk('nse_indices/data/'):
        print('i am here ass hole')

    for file in files:
        index = _NSE + file.split('.')[0]
        # result += index + '<br />'

        index_id = get_id_of_index(index)

        # for file in files:
            # print('i am here dick')
            # index = _NSE + file.split('.')[0];
            # result += result + index + '<br />'
            # print('chut ' + index)
    return HttpResponse(result)

def get_list_of_nse_indices():
    for roots, dirs, files in os.walk('nse_indices/data'):
        return files
def save_data_from_local(request):
    files = get_list_of_nse_indices()
    result = ''
    result += ('no of files ' + str(len(files)))
    i = 0;
    for file in files:
        i = i + 1
        if i > 20 or i >= len(files):
            break
        index_name = _NSE + file.split('.')[0]
        # index_id = get_id_of_index(index_name)
        df = pd.read_csv('nse_indices/data/'+ file)
        store_dataframe_database(df, index_name)
        # for j in range(0, len(df)):
        #     result += ('j  ' + str(df.iloc[j]) + '<br />')
        # result += '<br />' + 'str(index)' +'  ' + index_name + 'length of dataframe '+ str(len(df)) + '<br />'
    return HttpResponse('phew that was close' + result)


def make_the_row_proper(df_row, index_id):
    df_row.pop()
    df_row.append(index_id)
    df_row[0] = get_long_date(df_row[0])
    return df_row
def get_long_date(date_string):
        return int(math.floor(time.mktime(datetime.datetime.strptime(date_string, "%Y-%m-%d").timetuple())))



def store_dataframe_database(df, index):

    print('length of dataframe ' + str(len(df)) + 'index = ' + index)
    with connection.cursor() as cursor:
        index_id = get_id_of_index(index)
        if (index):
            for i in range(0,len(df)):
                df_row = make_the_row_proper(df.iloc[i].tolist()[:], index_id);
                for j in range(0, len(df_row)):
                    if type(df_row[j]).__name__ == 'float':
                        df_row[j] = round(df_row[j])

                cursor.execute("insert into daily_nse values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", df_row)

                print ('error in ' + str(j) + 'index ' + str(index))


def is_present(request, nse_index, start_date, end_date):

    print('hel')
    nse_index = ("nse/"+nse_index).upper();
    start_date_timestamp = get_long_date(start_date)
    end_date_timestamp = get_long_date(end_date)
    print('hel1')
    rows =  get_rows_from_database(nse_index, start_date_timestamp, end_date_timestamp)

    return HttpResponse(str(rows))

def get_rows_from_database(nse_index, start_date, end_date):
    json_array = []
    index = _NSE + nse_index
    index = get_id_of_index(nse_index)
    print('index ' + str(index) + 'string ' + nse_index)
    # print('start-date ' + str(start_date));
    print('in here rows from database ' + str(index) + ' start_date ' + str(start_date) + ' end_date ' + str(end_date))
    with connection.cursor() as cursor:
        # print('start-date long ' + start_date + 'long-date long '+ end_date)
        cursor.execute('select * from daily_nse where date >= %s and date <= %s and index = %s', [start_date, end_date, index])
        return cursor.fetchall()
    #     for row in rows:
    #         json_array.append(convert_nse_rows_to_json(row, nse_index))
    #
    #     print('heello there row leng    th ' + str(len(rows)))
    # return json.dumps(json_array)

def convert_nse_rows_to_json(row, nse_index):
    data = {}
    data['timestamp'] = row[0]
    data['open'] = row[1]
    data['high'] = row[2]
    data['low'] = row[3]
    data['last'] = row[4]
    data['close'] = row[5]
    data['total_trade_quantity'] = row[6]
    data['turnover'] = row[7]
    data['index_name'] = nse_index
    json_data = json.dumps(data)
    print(json_data)

def create_daily_indices_table(request):
    with connection.cursor() as cursor:
        cursor.execute('CREATE TABLE if not exists daily_nse(date numeric(15), open numeric(10, 2), high numeric(10, 2), low numeric(10, 2), last numeric(10, 2), close numeric(10, 2), total_trade_quantity numeric(10, 2), turnover numeric(10, 2), index integer NOT NULL, foreign key (index) references indices(id), constraint pk_daily_nse primary key (date, index))')
        cursor.execute('select count(*) from daily_nse')
        row = cursor.fetchone()
    result = 'count of row after operation ' + str(row[0])
    return HttpResponse(result)
