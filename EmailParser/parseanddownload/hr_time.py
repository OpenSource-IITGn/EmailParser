from dateutil.parser import *
from datetime import date
import datetime
import re

def get_time(time_lines):
    time_list = []
    for line in time_lines:
        k = re.search(r' \d+[-| |(to)|\d|(am)|(pm)|(AM)|(PM)|:]*[a|p|A|P][m|M]',line[0])
        try:
            time_list.append((k.group(0),line[1]))
        except:
            continue
    return time_list

def get_date_month(text, email_date,month):
    year = email_date.year
    if month+1 < email_date.month:
        year = year+1
    mon = ['January','February','March','April','May','June',
           'July','August','September','October','November','December']
    day = re.search(r'\d+',text)
    try:
        return day[0]+' '+mon[month]+' '+str(year)
    except:
        return mon[month]+' '+str(year)

def get_date_day(text, email_date, day):
    mon = ['January','February','March','April','May','June',
           'July','August','September','October','November','December']
    value = email_date.weekday()
    value = value - day
    if value < 0:
        value+=7
    if 'next' in text.lower():
        value+=7
    today = email_date+datetime.timedelta(days=value)
    return str(today.day)+' '+mon[today.month]+' '+str(today.year)

def get_date(date_lines, email_date):
    date_list = []
    for line in date_lines:
        #try:
        #    date_list.append((parse(line[0]),line[1]))
        #except:
        month = ['jan','feb','mar','apr','may','jun',
                   'jul','aug','sep','oct','nov','dec']
        day = ['monday','tuesday','wednesday','thrusday',
               'friday','saturday','sunday']
        for key in day+month:
            if key in line[0].lower():
                break
        else:
            break
        if key in month:
            date_list.append((get_date_month(line[0],email_date,month.index(key)),line[1]))
        else:
            date_list.append((get_date_day(line[0],email_date,day.index(key)),line[1]))
    return date_list

def get_info(lines,keyword):
    line_get_info = []
    for line in lines:
        for word in keyword:
            if word in line[0].lower():
                line_get_info.append(line)
                break
    return line_get_info


def get_lines(text):
    text = text.replace('Dr. ','Dr ')
    text = text.replace('Prof. ','Prof ')
    text = text.replace('Mr. ','Mr ')
    text = text.replace('Mrs. ','Mrs ')
    text = text.replace('  ',' ')
    temp_line = re.split(';|\. |\n|\*',text)
    lines = []
    i = 0
    for line in temp_line:
        line = line.replace('Dr ','Dr. ')
        line = line.replace('Prof ','Prof. ')
        line = line.replace('Mr ','Mr. ')
        line = line.replace('Mrs ','Mrs. ')
        lines.append((line.strip(),i))
        i+=1
    return lines

def __main__(text):
    keyword = ['date','monday','tuesday','wednesday','thrusday','friday',
               'saturday','sunday','january','february','march','april','may','june','july',
               'august','september','october','november','december']
    print(get_date((get_info(get_lines(text),keyword)),datetime.date(2018,12,12)))
    keyword = ['time','am','pm']
    time_lines = get_info(get_lines(text),keyword)
    keyword = ['1','2','3','4','5','6','7','8','9','0']
    time_lines = get_info(time_lines[:],keyword)
    print(get_time(time_lines))
    

#text = """
#"""
#__main__(text)