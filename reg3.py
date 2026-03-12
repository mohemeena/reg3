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

    # Setting previous searches from cookies
    set_cookies(prev_dept)
    set_cookies(prev_coursenum)
    set_cookies(prev_area)
    set_cookies(prev_title)

    # Get the department inquiry
    dept = get_inquiry(dept)
    if dept == '':
        prev_dept = '(None)'

    # Get the course number inquiry
    coursenum = get_inquiry(coursenum)
    if coursenum == '':
        prev_coursenum = '(None)'

    # Get the area inquiry
    area = get_inquiry(area)
    if area == '':
        prev_area = '(None)'

    # Get the title inquiry
    title = get_inquiry(title)
    if title == '':
        prev_title = '(None)'

    query = {
        'dept': dept,
        'coursenum': coursenum,
        'area': area,
        'title': title
    }

    overviews_output = database.get_overviews(query)

    if overviews_output[0] is True:
        html_code = flask.render_template('classoverviews.html',
            prev_dept=prev_dept, prev_coursenum=prev_coursenum,
            prev_area=prev_area, prev_title=prev_title,
            overviews = overviews_output[1])
        response = flask.make_response(html_code)
    
    else:
        html_code = flask.render_template('error.html',
            error_message = overviews_output[1])
        response = flask.make_response(html_code)
    
    return response


#-----------------------------------------------------------------------
# Course Details Page:
#-----------------------------------------------------------------------
@app.route('/regdetails?classid={{ course.classid }}', methods={'GET'})

def classdetails():

    classid = get_inquiry(classid)

    if classid is None or classid == ' ':
        html_code = flask.render_template(
            'error.html',
            error_message=f'no class with class id {classid} found'
        )
        response = flask.make_response(html_code)
        return response

    details_output = database.get_details(classid)

    if details_output[0] is True:
        html_code = flask.render_template('regdetails.html',
            coursedetails = details_output[1])
        response = flask.make_response(html_code)
    
    else:
        html_code = flask.render_template('error.html',
            error_message = details_output[1])
        response = flask.make_response(html_code)
    
    return response

#-----------------------------------------------------------------------
# Helper Functions:
#-----------------------------------------------------------------------

def set_cookies(arg):
    arg = flask.request.cookies.get('{arg}')
    if arg is None:
        arg = '(None)'

def get_inquiry(arg):
    arg = flask.request.args.get('{arg}')
    if arg is None:
        arg = ''
    arg = arg.strip()
    return arg

#-----------------------------------------------------------------------