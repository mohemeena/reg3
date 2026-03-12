#-----------------------------------------------------------------------
# runserver.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import sys
import reg3

def main():
    
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} port', file = sys.stderr)
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except Exception:
        print(f'{sys.argv[0]}: Port must be an integer.',
            file = sys.stderr)
        sys.exit(1)

    try:
        reg3.app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as ex:
        print(f'{sys.argv[0]}: {ex}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
