#-----------------------------------------------------------------------
# testregoverviews.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import sys
import argparse
import playwright.sync_api

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def get_args():

    parser = argparse.ArgumentParser(
        description='Test the ability of the reg application to '
            + 'handle "primary" (class overviews) queries')

    parser.add_argument(
        'serverURL', metavar='serverURL', type=str,
        help='the URL of the reg application')

    parser.add_argument(
        'browser', metavar='browser', type=str,
        choices=['firefox', 'chrome'],
        help='the browser (firefox or chrome) that you want to use')

    args = parser.parse_args()

    return (args.serverURL, args.browser)

#-----------------------------------------------------------------------

def print_flush(message):

    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def run_test(server_url, browser_process, input_values):

    print_flush(UNDERLINE)
    for key, value in input_values.items():
        print_flush(key + ': |' + value + '|')

    try:
        page = browser_process.new_page()
        page.goto(server_url)

        dept_input = page.locator('#deptInput')
        coursenum_input = page.locator('#coursenumInput')
        area_input = page.locator('#areaInput')
        title_input = page.locator('#titleInput')

        dept_input.fill(input_values.get('dept', ''))
        coursenum_input.fill(input_values.get('coursenum', ''))
        area_input.fill(input_values.get('area', ''))
        title_input.fill(input_values.get('title', ''))

        button = page.locator('#submitButton')
        button.click()

        overviews_table = page.locator('#overviewsTable')
        print_flush(overviews_table.inner_text())

    except Exception as ex:
        print(str(ex), file=sys.stderr)

#-----------------------------------------------------------------------

def main():

    server_url, browser = get_args()

    with playwright.sync_api.sync_playwright() as pw:

        if browser == 'chrome':
            browser_process = pw.chromium.launch()
        else:
            browser_process = pw.firefox.launch()

        run_test(server_url, browser_process,
            {'dept':'COS'})

        run_test(server_url, browser_process,
            {'dept':'COS', 'coursenum':'2', 'area':'qr',
            'title':'intro'})

        # Add more tests here.
       
        # assignment spec tests
        run_test(server_url, browser_process,
            {'title':'Independent Study'})

        run_test(server_url, browser_process,
            {'title':'Independent Study '})

        run_test(server_url, browser_process,
            {'title':'Independent Study  '})

        run_test(server_url, browser_process,
            {'title':' Independent Study'})

        run_test(server_url, browser_process,
            {'title':'  Independent Study'})

        run_test(server_url, browser_process,
            {'dept':'COS', 'coursenum':'3'})
        
        run_test(server_url, browser_process,
            {'area':'qr'})
        
        run_test(server_url, browser_process,
            {'area':'Qr'})
        
        run_test(server_url, browser_process,
            {'area':'-a '})
        
        run_test(server_url, browser_process,
            {'area':'qr st'})
        
        run_test(server_url, browser_process,
            {'area':' '})
        
        run_test(server_url, browser_process,
            {'area':'qr', 'dept': ''})
        
        run_test(server_url, browser_process,
            {'area':'', 'dept': 'cos'})
        
        run_test(server_url, browser_process,
            {'dept': '-x'})

        run_test(server_url, browser_process,
            {'dept':'cos', 'area':'qr'})

        #long titles
        run_test(server_url, browser_process,
            {'title':'Studies in Religion and Philosophy: Religion'
            ' & the Fragility of American Democracy: Emerson & Baldwin'})

        run_test(server_url, browser_process,
            {'title':'African American History from '
            'Reconstruction to'})

        # wildcard characters 
        run_test(server_url, browser_process,
            {'title':'C_S'})

        run_test(server_url, browser_process,
            {'title':'c%s'})

        run_test(server_url, browser_process,
            {'title':'-c'})

        # blank input test
        run_test(server_url, browser_process, {})

        # empty / space fields
        run_test(server_url, browser_process,
            {'dept':' '})

        run_test(server_url, browser_process,
            {'coursenum':' '})

        run_test(server_url, browser_process,
            {'title':' '})

        # invalid formatting
        run_test(server_url, browser_process,
            {'coursenum':'hi'})

        run_test(server_url, browser_process,
            {'coursenum':'9 8'})
        
if __name__ == '__main__':
    main()
