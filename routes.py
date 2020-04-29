from flask import Flask, render_template, flash, request, url_for, redirect, Markup
from flask_bootstrap import Bootstrap
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import lib

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

sqlite_file = 'useful_data.sqlite'

@app.route('/',  methods=['GET', 'POST'])
def chart():


    start_date = "2019-02-19"
    end_date= "2020-01-10"
    interval = "month"


    total, success, fail, warning = lib.chart_details(sqlite_file, (start_date, end_date), "percentage")
    chart_conf = lib.chart_global(sqlite_file, start_date, end_date, interval)
    donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")


    if request.method == 'POST':

        start_date = request.values.get('date_from')
        end_date = request.values.get('date_to')
        interval = request.values.get('scale')

        try:
            total, success, fail, warning = lib.chart_details(sqlite_file, (start_date, end_date), "percentage")
            chart_conf = lib.chart_global(sqlite_file, start_date, end_date, interval)
            donut_courses = lib.chart_courses(sqlite_file, (start_date, end_date), "pourcentage")
        except:
            pass

        return render_template('index.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval)

    else:
      return render_template('index.html', total = total, success = success, fail = fail, warning = warning, chart_global = chart_conf, donut_courses = donut_courses, start_date_keep=start_date, end_date_keep=end_date, scale_keep=interval)





app.run(debug=True, port = 80)
