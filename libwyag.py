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
        case "checkout" : cmd_commit(args)
        case "hash-object" : cmd_hash_object(args)
        case "init" : cmd_init(args)
        case "log" : cmd_log(args)
        case "ls-files" : cmd_ls_files(args)
        case "ls-tree"  : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"   : cmd_rm(args)
        case "show-ref" : cmd_show_ref(args)
        case "status"   : cmd_status(args)
        case "tag"  : cmd_tag(args)
        case _ : print("Bad command.")

class GitRepository (object):
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None


    # repo init function, force = optional argument that disables all checks
    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")
        
        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")
        
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception(f"Unsupported repositoryformatversion: {vers}")

