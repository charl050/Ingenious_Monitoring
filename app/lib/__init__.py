import sqlite3
from calendar import monthrange


class Date:

    def __init__(self,date):
        """
        pre date(str)
        """
        self.day = date[8:10]
        self.month = date[5:7]
        self.year = date[:4]

    def __eq__(self,other):
        """
        pre (Date) : a Date object
        return (bool) : "other" is the same date than "self"
        """
        if self.day == other.day and self.month == other.month and\
        self.year == other.year:
            return True
        return False

    def __ge__(self, other):
        """
        pre (Date) : a Date object
        return (bool) : "self" is greater or equal than "other"
        """
        if int(self.year) < int(other.year):
            return False
        if  int(self.year) == int(other.year) and int(self.month) <\
         int(other.month):
            return False
        if  int(self.year) == int(other.year) and int(self.month) == \
        int(other.month) and int(self.day) < int(other.day):
            return False
        return True

    def __lt__(self, other):
        """
        pre (Date) : a Date object
        return (bool) : "self" is lower than "other"
        """
        if int(self.year) > int(other.year):
            return False
        if  int(self.year) == int(other.year) and int(self.month) >\
         int(other.month):
            return False
        if  int(self.year) == int(other.year) and int(self.month) == \
        int(other.month) and int(self.day) >= int(other.day):
            return False
        return True

    def __le__(self, other):
        """
        pre (Date) : a Date object
        return (bool) : "self" is lower or equal than "other"
        """
        if int(self.year) > int(other.year):
            return False
        if  int(self.year) == int(other.year) and int(self.month) >\
         int(other.month):
            return False
        if  int(self.year) == int(other.year) and int(self.month) == \
        int(other.month) and int(self.day) > int(other.day):
            return False
        return True

    def __str__(self):
        return "{}/{}/{}".format(self.day,self.month,self.year)


def dates(sqlite_file, start_date, end_date):
    """
    pre sqlite_file(str) : sqlite file
    pre start_date(str) : start date like xx/yy/zzzz
    pre end_date(str) : end date like xx/yy/zzzz
    return (list) : every different dates in string format from sqlite file
    """
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #turn "from" and "to" into Date objects
    #(Date object whill be usefull to compare different dates and to be able to
    #sort them out)
    start_date = Date(start_date[6:]+"-"+start_date[3:5]+"-"+start_date[:2])
    end_date = Date(end_date[6:]+"-"+end_date[3:5]+"-"+end_date[:2])
    #turn every different dates into Date object and put them in a list
    dates_object = []
    print("scanning lines ... ")
    print("It can take some time ... ")
    #browse the file
    for date in cursor.execute("SELECT submitted_on from submissions"):
        date = Date(date[0][:10])
        #keep dates between start_date and end_date
        if date not in dates_object and date >= start_date and date <= end_date:
            dates_object.append(date)
    #if start and end dates not in dates list, add them
    if start_date not in dates_object:
        dates_object.append(start_date)
    elif end_date not in dates_object:
        dates_object.append(end_date)
    #sort list of Dates object
    dates_object.sort()
    #turn every Dates object into str and put them in a list
    dates_string = []
    for date_object in dates_object:
        dates_string.append(str(date_object))
    return dates_string

def calc_intervals(dates, interval):
    """
    pre dates(list) : liste of dates like [xx/yy/zzzz]
    pre interval(int) : interval between two dates :
                        0 = day
                        1 = month
                        2 = year
    return (list) : list of interal
    """
    intervals = []
    #day interval
    if interval == 0:
        for date in dates:
            intervals.append((date,date))
        return intervals
    #month interval
    elif interval == 1:
        first_d =  dates[0]
        last_d = dates[-1]
        #while first_d month is different from last_d month
        while first_d[3:] != last_d[3:]:
            #add the first day and the last day in month in intervals list
            current_month = int(first_d[3:5])
            days_in_month = monthrange(2019, current_month)[1]
            intervals.append((first_d,str(days_in_month)+first_d[2:]))
            #first_d = first day of next_month
            if current_month > 11:
                next_month = "01"
                year = str(int(first_d[6:])+1)
            else:
                next_month = str(current_month+1)
                if len(next_month) == 1:
                    next_month = "0"+next_month
                year = first_d[6:]
            first_d = "01/"+next_month+"/"+year
        #add the first day and the last day in intervals list
        intervals.append((first_d,last_d))
        return intervals
    #year interval
    elif interval == 2:
        first_d =  dates[0]
        last_d = dates[-1]
        #while first_d year is different year last_d month
        while first_d[6:] != last_d[6:]:
            #add the first day and the last day in year in intervals list
            end_year = "31/12/"+first_d[6:]
            intervals.append((first_d,end_year))
            #first_d = first day of next_year
            next_year = str(int(first_d[6:])+1)
            first_d = "01/01/"+next_year
        ##add the first day and the last day in intervals list
        intervals.append((first_d,last_d))
        return intervals
    else:
        raise Exception("No interval = {}".format(interval))

def courses(sqlite_file):
    """
    pre sqlite_file(str) : sqlite file
    return (list) : every different courses in string format from sqlite file
    """
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    courses = [] # list of courses
    print("scanning lines ... ")
    print("It can take some time ... ")
    #browse the file
    for row in cursor.execute("SELECT course from submissions"):
        course = row[0]
        if course not in courses :
            courses.append(course)
    return courses


def results_submissions(sqlite_file, interval):
    """
    pre sqlite_file(str) : sqlite file
    pre interval(tuple) : a interval like (xx/yy/zzzz, xx/yy/zzzz,)
    return (tuple) : (total_count,success_count,faile)
    return (tuple) : (total_count,success_count,failed_count,error_count)
    """
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    #intervals
    first_d = Date(interval[0][6:]+"-"+interval[0][3:5]+"-"+interval[0][:2])
    last_d = Date(interval[1][6:]+"-"+interval[1][3:5]+"-"+interval[1][:2])
    #counts
    total_count = 0
    success_count = 0
    failed_count = 0
    error_count = 0
    print("scanning lines ... ")
    #browse the file
    for row in cursor.execute("SELECT submitted_on, result from submissions"):
        #turn every different dates into Date
        #(Date object is usefull to turn date_row in xx/yy/zzzz format)
        row_date = Date(row[0][:10])
        #check if row_date is in interval chosen in ragument
        if row_date >= first_d and row_date <= last_d:
            total_count += 1 # add 1 to total_count
            #add 1 in according to the result of submissions
            row_result = row[1]
            if row_result == "success":
                success_count += 1
            elif row_result == "failed":
                failed_count += 1
            else:
                error_count += 1
    return (total_count,success_count,failed_count,error_count)

def course_submissions(sqlite_file, interval):
    """
    pre sqlite_file(str) : sqlite file
    pre interval(tuple) : a interval like (xx/yy/zzzz, xx/yy/zzzz,)
    return (dict) : {"<course_name>":<number_of_submissions>}
    """
    #reach to file
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    result = {}
    #intervals
    first_d = Date(interval[0][6:]+"-"+interval[0][3:5]+"-"+interval[0][:2])
    last_d = Date(interval[1][6:]+"-"+interval[1][3:5]+"-"+interval[1][:2])
    #browse the file
    for row in cursor.execute("SELECT submitted_on, course from submissions"):
        #turn every different dates into Date
        #(Date object is usefull to turn date_row in xx/yy/zzzz format)
        row_date = Date(row[0][:10])
        #check if row_date is in interval chosen in ragument
        if row_date >= first_d and row_date <= last_d:
            if result.get(row[1],0) == 0:
                result[row[1]] = 1
            else:
                result[row[1]] += 1
    return result

def percentage(data_list):
    """
    pre data_list(list/tuple)
    return (list) : the percentage for each data
    """
    result = []
    #count the number of elements
    total_elements = 0
    for data in data_list:
        total_elements += data
    #put the purcentages of element in list
    for data in data_list:
        result.append(data/total_elements*100)
    return result

def percentage_dict(data_dict):
    """
    pre data_dict(dict) : dict with int for values
    return (dict) : the percentage for each data
    """
    result = {}
    #count the number of elements
    total_elements = 0
    for key in data_dict:
        total_elements += data_dict[key]
    for key in data_dict:
        result[key] = data_dict[key]/total_elements*100
    return result
