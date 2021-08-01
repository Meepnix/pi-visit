"""The main routine of siginin-pi."""

import sys
import os


from signin_pi.scan import scan


def main(args=None):
    """The main routine."""

    import signin_pi.scan

    from dotenv import load_dotenv
    import mariadb

    load_dotenv()

    if args is None:
        args = sys.argv[1:]

    print("This is the main routine meep.")


    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'],
            host=os.environ['DB_HOST'],
            port=int(os.environ['DB_PORT']),
            database=os.environ['DB_DATABASE']

        )   
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cur = conn.cursor()

    checkTableExists(conn, "")
    #scan.scan_qr()

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.


def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_name = '{0}'
    """.format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    print("found nothin")
    return False

if __name__ == "__main__":
    sys.exit(main())




