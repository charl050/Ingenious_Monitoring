from app import *
from app import lib
import json
from flask import Markup
from flask_socketio import SocketIO
import random




app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

"""

database = 'inginious.sqlite'
date = lib.dates(database, "03/02/2019", "11/01/2020")
interval = list(lib.calc_intervals(date, 1))
data = []
background_color = []
border_color = []

"""

def random_rgb(border=False):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    if border:
        return 'rgba({}, {}, {}, {})'.format(r,g,b,0.8)

    else:
        return 'rgba({}, {}, {}, {})'.format(r,g,b,0.2)




def chart_setup(type, labels, datas, background_color, border_color, extra_options=None):

    label = []
    data = []
    backgroundColor = []
    borderColor = []

    for i in labels:
        label.append(i)
    for i in datas:
        data.append(i)
    for i in background_color:
        backgroundColor.append(i)
    for i in border_color:
        borderColor.append(i)
    print()

    if extra_options is not None:
        return Markup("{{ 'type': '{0}',  'data': {{ 'labels': {1}, 'datasets': [{{ 'data': {2}, 'backgroundColor': {3}, 'borderColor': {4} }}] }}, 'options' : {5} }}".format(type, labels, datas, background_color, border_color,extra_options))
    else:
        return Markup("{{ 'type': '{0}',  'data': {{ 'labels': {1}, 'datasets': [{{ 'data': {2}, 'backgroundColor': {3}, 'borderColor': {4} }}] }} }}".format(type, labels, datas, background_color, border_color))

def chart_global(database):
    date = lib.dates(database, "03/02/2019", "11/01/2020")
    interval = list(lib.calc_intervals(date, 1))
    data = []
    background_color = []
    border_color = []


    for i in range(len(interval)):
        data.append(lib.results_submissions(database, interval[i])[0])
        background_color.append(random_rgb())
        border_color.append(random_rgb(True))

    conf = chart_setup(type = 'bar', labels = interval, datas = data, background_color = background_color, border_color = border_color, extra_options = "{ 'onClick' : click_labels }")


    return conf

def chart_global1(sqlite_file, start_date, end_date, interval):
    """
    pre sqlite_file(str) : sqlite file
    pre start_date(str) : start date like xx/yy/zzzz
    pre end_date(str) : end date like xx/yy/zzzz
    pre interval(int) : interval between two dates :
                        0 = day
                        1 = month
                        2 = year
    return (list) : chart_setup of data
    """
    #init intervals
    d = lib.dates(sqlite_file, "03/02/2019", "11/01/2020")
    i = lib.calc_intervals(d, 1)
    #init labels
    labels_list = []
    for interv in i:
        labels_list.append(interv[0]+"-"+interv[1])
    #init datas
    datas_list = []
    background_color = []
    border_color = []
    for interv in i:
        r_s = lib.results_submissions(sqlite_file, interv)
        datas_list.append(r_s[0])
        background_color.append(random_rgb())
        border_color.append(random_rgb(True))

    conf = chart_setup(type = 'bar', labels = labels_list, datas = datas_list, background_color = background_color, border_color = border_color, extra_options = "{ 'onClick' : click_labels }")
    return conf


def chart_details(sqlite_file, interval):
    """
    pre sqlite_file(str) : sqlite file
    pre interval(tuple) : a interval like (xx/yy/zzzz-xx/yy/zzzz)
    return (list) : chart_setup of data
    """
    interval = tuple(interval.split('-'))
    r_s = lib.results_submissions(sqlite_file, interval)
    return chart_setup(type = 'pie', labels = ['fail','success','errors'], datas = list(r_s[1:]), background_color = [random_rgb(),random_rgb(),random_rgb()], border_color = [random_rgb(True),random_rgb(True),random_rgb(True)], extra_options= None)
#test = chart_setup(type = 'bar', labels = ['aaaaaaaaa','bdadsdasds','sdsadadasc','ddadsadasd'], datas = [1,2,3,4], background_color = ['rgba(255, 206, 86, 0.2)','rgba(255, 206, 86, 0.2)','rgba(255, 206, 86, 0.2)','rgba(255, 206, 86, 0.2)'], border_color = ['rgba(255, 206, 86, 0.2)','rgba(255, 206, 86, 0.2)','rgba(255, 206, 86, 0.2)','rgba(255, 206, 86, 0.2)'], extra_options = "{ 'onClick' : click_labels }")
test1 =1


test = chart_global1("inginious.sqlite", "03/02/2019", "11/01/2020", 1)

@app.route('/')
def chart():
    #vars = {'123' : '123'}
    return render_template('index.html', id = Markup("'chart1'"), data = test, id1 = Markup("'chart2'"), data1 = test1 ) #, vars = appDict)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['POST']):
    print('received my event: ' + str(json))
    j = chart_details("inginious.sqlite", json)

    socketio.emit('reply', j)
    print('ok')




socketio.run(app, port = 80, debug = True )
