#-----------------------------------------------------------------------
# runserver.py
# Author: Mohemeen Ahmed and Amel Osman
#-----------------------------------------------------------------------

import sys
import reg3
import argparse

def main():
    
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} port', file = sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description="The registrar application")

    parser.add_argument("-h", "--help",
    help="show this help message and exit", default = "")

    parser.add_argument("port",type=int,
    help=" the port at which the server is listening")

    args = parser.parse_args()

    try:
        reg3.app.run(host='0.0.0.0', port=args.port, debug=True)
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
