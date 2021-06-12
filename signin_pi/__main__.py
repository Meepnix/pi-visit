"""The main routine of siginin-pi."""

import sys


def main(args=None):
    """The main routine."""

    from scan import scan_qr

    if args is None:
        args = sys.argv[1:]

    print("This is the main routine.")

    scan_qr()



    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.


if __name__ == "__main__":
    sys.exit(main())
