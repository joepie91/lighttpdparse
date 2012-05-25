import re, argparse, os

parser = argparse.ArgumentParser(description='Parse a lighttpd access log.')

parser.add_argument('logfile', metavar='logfile', type=str, nargs='+',
                   help='path(s) of the logfile(s)')
                   
args = parser.parse_args()
options = vars(args)
