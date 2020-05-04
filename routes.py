from flask import Flask, render_template, flash, request, url_for, redirect, Markup
from flask_bootstrap import Bootstrap
import lib

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(__name__)
sqlite_file = 'useful_data.sqlite'

# The fonction for the home page
@app.route('/',  methods=['GET', 'POST'])
def index():

    # Default values
    start_date = "2019-02-19"
    end_date= "2020-01-10"
    interval = "month"


    total, success, fail, warning = lib.chart_details(sqlite_file, (start_date, end_date), "percentage")
    chart_conf = lib.chart_global(sqlite_file, start_date, end_date, interval)
    donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")


    if request.method == 'POST':

        # If the user send a post request, get the inputs
        start_date = request.values.get('date_from')
        end_date = request.values.get('date_to')
        interval = request.values.get('scale')

        try: # Try to prevent attack from the user
            total, success, fail, warning = lib.chart_details(sqlite_file, (start_date, end_date), "percentage")
            chart_conf = lib.chart_global(sqlite_file, start_date, end_date, interval)
            donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")
        except:
            pass

        # Return values to the template
        return render_template('index.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval)

    else:
      return render_template('index.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval)


# Fonction for the course page
@app.route('/courses',  methods=['GET', 'POST'])
def courses():
    start_date = "2019-02-19"
    end_date= "2020-01-10"
    interval = "month"
    course = 'LSINF1252'


    total, success, fail, warning = lib.chart_details_courses(sqlite_file, (start_date, end_date), "percentage", course)
    chart_conf = lib.chart_global_courses(sqlite_file, start_date, end_date, interval, course)
    donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")
    donut_tasks = lib.chart_task(sqlite_file, (start_date, end_date), "pourcentage", course)


    if request.method == 'POST':

        course = request.values.get('course')

        start_date = request.values.get('date_from')
        end_date = request.values.get('date_to')
        interval = request.values.get('scale')

        try:
            total, success, fail, warning = lib.chart_details_courses(sqlite_file, (start_date, end_date), "percentage", course)
            chart_conf = lib.chart_global_courses(sqlite_file, start_date, end_date, interval, course)
            donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")
            donut_tasks = lib.chart_task(sqlite_file, (start_date, end_date), "pourcentage", course)

        except:
            pass

        return render_template('courses.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_tasks = donut_tasks, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval, course_keep = course)

    else:
      return render_template('courses.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_tasks = donut_tasks, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval, course_keep = course)




app.run(debug=True, port = 80)
