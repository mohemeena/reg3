#-----------------------------------------------------------------------
# reg3.py
# Authors: Amel Osman & Mohemeen Ahmed
#-----------------------------------------------------------------------

import flask
import database

#-----------------------------------------------------------------------
app = flask.Flask(__name__, template_folder='.')
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
# Class Overviews Page (Home Page):
#-----------------------------------------------------------------------
@app.route('/', methods={'GET'})
@app.route('/classoverviews', methods={'GET'})
def classoverviews():

    # Get the department inquiry
    dept = flask.request.args.get('dept')
    if dept is None:
        dept = ''
    dept = dept.strip()
    
    if dept == '':
        prev_dept = ''
    else:
        prev_dept = dept

    # Get the course number inquiry
    coursenum = flask.request.args.get('coursenum')
    if coursenum is None:
        coursenum = ''
    coursenum = coursenum.strip()
    
    if coursenum == '':
        prev_coursenum = ''
    else:
        prev_coursenum = coursenum

    # Get the area inquiry
    area = flask.request.args.get('area')
    if area is None:
        area = ''
    area = area.strip()
    
    if area == '':
        prev_area = ''
    else:
        prev_area = area

    # Get the title inquiry
    title = flask.request.args.get('title')
    if title is None:
        title = ''
    title = title.strip()
    
    if title == '':
        prev_title = ''
    else:
        prev_title = title

    query = {
        'dept': dept,
        'coursenum': coursenum,
        'area': area,
        'title': title
    }

    overviews_output = database.get_overviews(query)

    if overviews_output[0] is True:
        html_code = flask.render_template('classoverviews.html',
            dept=prev_dept, coursenum=prev_coursenum,
            area=prev_area, title=prev_title,
            overviews = overviews_output[1])
        response = flask.make_response(html_code)
    
    else:
        html_code = flask.render_template('error.html',
            error_message = overviews_output[1])
        response = flask.make_response(html_code)
    
    # Set cookies
    response.set_cookie('prev_dept', prev_dept)
    response.set_cookie('prev_coursenum', prev_coursenum)
    response.set_cookie('prev_area', prev_area)
    response.set_cookie('prev_title', prev_title)

    return response


#-----------------------------------------------------------------------
# Course Details Page:
#-----------------------------------------------------------------------
@app.route('/regdetails', methods={'GET'})

def classdetails():

    # Getting previous searches from cookies
    prev_dept = flask.request.cookies.get('prev_dept')
    if prev_dept is None:
        prev_dept = flask.request.cookies.get('prev_dept','')

    prev_coursenum = flask.request.cookies.get('prev_coursenum')
    if prev_coursenum is None:
        prev_coursenum = flask.request.cookies.get('prev_coursenum','')

    prev_area = flask.request.cookies.get('prev_area')
    if prev_area is None:
        prev_area = flask.request.cookies.get('prev_area','')

    prev_title = flask.request.cookies.get('prev_title')
    if prev_title is None:
        prev_title = flask.request.cookies.get('prev_title','')

    classid = flask.request.args.get('classid')

    if classid is None or classid == ' ':
        html_code = flask.render_template(
            'error.html',
            error_message=f'no class with class id {classid} found',
        )
        response = flask.make_response(html_code)
        return response

    details_output = database.get_details(classid)

    if details_output[0] is True:
        html_code = flask.render_template('regdetails.html',
            coursedetails = details_output[1],
            dept=prev_dept, coursenum=prev_coursenum,
            area=prev_area, title=prev_title)
        response = flask.make_response(html_code)
    
    else:
        html_code = flask.render_template('error.html',
            error_message = details_output[1])
        response = flask.make_response(html_code)
    
    return response

