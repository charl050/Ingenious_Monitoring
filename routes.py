from flask import Flask, render_template, flash, request, url_for, redirect, Markup
from flask_bootstrap import Bootstrap
import lib

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(__name__)
sqlite_file = 'useful_data.sqlite'
sqlite_file_1 = 'inginious.sqlite'

# The function for the home page
@app.route('/',  methods=['GET', 'POST'])
def index():

    # Default values
    start_date = "2019-02-19"
    end_date = "2020-01-10"
    interval = "month"


    total, success, fail, warning = lib.chart_details(sqlite_file, (start_date, end_date), "percentage")
    chart_conf = lib.chart_global(sqlite_file, start_date, end_date, interval)
    donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")


    if request.method == 'POST':

        # If the user send a post request, get the inputs
        start_date = request.values.get('date_from')
        end_date = request.values.get('date_to')
        interval = request.values.get('scale')

        try: # Try to prevent bad inputs from the user
            total, success, fail, warning = lib.chart_details(sqlite_file, (start_date, end_date), "percentage")
            chart_conf = lib.chart_global(sqlite_file, start_date, end_date, interval)
            donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")

            return render_template('index.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval, error = None)


        except:
            # Return error alert
            return render_template('index.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval, error = True)

    else:
      return render_template('index.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval, error = None)


# Function for the detailed page
@app.route('/details',  methods=['GET', 'POST'])
def details():

    start_date = "2019-02-19"
    end_date= "2020-01-10"
    interval = "month"
    course = 'LSINF1252'
    task = 'All'
    list = ['LSINF1101_PYTHON', 'LEPL1402', 'LSINF1252']
    task_item = ['All'] + lib.tasks(sqlite_file_1, (start_date, end_date))[list.index(course)]
    leng = len(task_item)


    total, success, fail, warning = lib.chart_details_courses(sqlite_file, (start_date, end_date), "percentage", course)
    chart_conf = lib.chart_global_courses(sqlite_file, start_date, end_date, interval, course)
    donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")
    donut_tasks = lib.chart_task(sqlite_file, (start_date, end_date), "pourcentage", course)


    if request.method == 'POST':

        course = request.values.get('course')
        task = request.values.get('task')

        start_date = request.values.get('date_from')
        end_date = request.values.get('date_to')
        interval = request.values.get('scale')


        try:
            if task != 'All':
                task_item = ['All'] + lib.tasks(sqlite_file_1, (start_date, end_date))[list.index(course)]
                leng = len(task_item)
                total, success, fail, warning = lib.chart_details_task(sqlite_file_1, (start_date, end_date), "percentage",course, task)
                chart_conf = lib.chart_global_task(sqlite_file, start_date, end_date, interval, task, course)

            else:
                task_item = ['All'] + lib.tasks(sqlite_file_1, (start_date, end_date))[list.index(course)]
                leng = len(task_item)
                total, success, fail, warning = lib.chart_details_courses(sqlite_file, (start_date, end_date), "percentage", course)
                chart_conf = lib.chart_global_courses(sqlite_file, start_date, end_date, interval, course)
                donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")
                donut_tasks = lib.chart_task(sqlite_file, (start_date, end_date), "pourcentage", course)

            return render_template('details.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_tasks = donut_tasks, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval, course_keep = course, task_keep = task, len = leng, task_item = task_item, error = None)


        except :
            return render_template('details.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_tasks = donut_tasks, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval, course_keep = course, task_keep = task, len = leng, task_item = task_item, error = True)



    else:
      return render_template('details.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_tasks = donut_tasks, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval, course_keep = course, task_keep = task, len = leng, task_item = task_item, error = None)


app.run(debug=True, port = 80)
