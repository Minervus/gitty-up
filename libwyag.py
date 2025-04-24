import argparse # For parsing command-line arguments
import configparser # for read and write config files
from datetime import datetime 
import grp, pwd # for reading the user/group database on unix 
from fnmatch import fnmatch # for .gitignore - matching filenames like *.txt
import hashlib # for the SHA-1 function
from math import cell 
import os # for filesystem stuff
import re # regex
import sys # for accessing command line arguments e.g. sys.argv
import zlib # for compressing 

argparser = argparse.ArgumentParser(description="The content tracker")

# Handling subcommands
argparsers = argparser.add_subparsers(title="Commands", dest="command")
argparsers.required = True

# dest="command" will return the command as a string
# now we find the string and the correct function

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add"  : cmd_add(args)
        case "cat-file" : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)