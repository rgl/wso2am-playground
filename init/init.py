#!/bin/python3

import argparse
import logging
import sys
import textwrap
import urllib3
import wso2am


def main():
    # see https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
    urllib3.disable_warnings()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            init.

            example:

            python3 %(prog)s -v wso2am-init
            '''))
    parser.add_argument(
        '--verbose',
        '-v',
        default=0,
        action='count',
        help='verbosity level. specify multiple to increase logging.')
    subparsers = parser.add_subparsers(help='sub-command help')
    wso2am_init_parser = subparsers.add_parser('wso2am-init', help='initialize wso2am')
    wso2am_init_parser.add_argument(
        '--base-url',
        default='https://wso2am.test:9443',
        help='base wso2am url')
    wso2am_init_parser.set_defaults(sub_command=wso2am.init_main)
    wso2am_try_parser = subparsers.add_parser('wso2am-try', help='execute ad-hoc wso2am requests')
    wso2am_try_parser.add_argument(
        '--base-url',
        default='https://wso2am.test:9443',
        help='base wso2am url')
    wso2am_try_parser.set_defaults(sub_command=wso2am.try_main)
    args = parser.parse_args()

    LOGGING_FORMAT = '%(asctime)-15s %(levelname)s %(name)s: %(message)s'
    if args.verbose >= 3:
        logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)
        from http.client import HTTPConnection
        HTTPConnection.debuglevel = 1
    elif args.verbose >= 2:
        logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)
    elif args.verbose >= 1:
        logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)

    return args.sub_command(args)


if __name__ == '__main__':
    sys.exit(main())
