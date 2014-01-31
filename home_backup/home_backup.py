#!/usr/bin/env python

import os
from shutil import rmtree
import argparse
import logging
from sh import rsync


#Parse arguments
parser = argparse.ArgumentParser(
    description=__doc__)

parser.add_argument("BACKUPDIR", help="Specify the directory to backup.")
parser.add_argument("DESTINATIONDIR", help="Specify the directory where the backup is stored.")
parser.add_argument("-t", "--trash", help="Delete unnecessary files and empty the trash.", action="store_true")
parser.add_argument("-e", "--exclude", help="Exlude the following directories from backup.", action="append")
parser.add_argument("-l", "--logfile", help="Specify the logfile to monitor.")
parser.add_argument("-q", "--quiet", help="Do not print to stdout.", action="store_true")

args = parser.parse_args()

# Define variables
backupdir = args.BACKUPDIR
destinationdir = args.DESTINATIONDIR
logfile = args.logfile

#Logging
rootLogger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s - %(message)s")
rootLogger.setLevel(logging.INFO)
if logfile:
    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

if not args.quiet:
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)


# directory exist-check
def check_dir_exist(os_dir):
    if not os.path.exists(os_dir):
        logging.error("{} does not exist.".format(os_dir))
        exit(1)

check_dir_exist(backupdir)

# delete function
def delete_files(ending, indirectory):
    for r, d, f in os.walk(indirectory):
        for files in f:
            if files.endswith("." + ending):
                try:
                    os.remove(os.path.join(r, files))
                    logging.info("Deleting {}/{}".format(r, files))
                except OSError:
                    logging.warning("Could not delete {}/{}".format(r, files))
                    pass


# Delete actual files first
if args.trash:
    file_types = ["tmp", "bak", "dmp"]
    for file_type in file_types:
        delete_files(file_type, backupdir)
    # Empty trash can
    try:
        rmtree(os.path.expanduser("~/.local/share/Trash/files"))
    except OSError:
        logging.warning("Could not empty the trash or trash already empty.")
        pass

# handle exclusions
exclusions = []
if args.exclude:
    for argument in args.exclude:
        exclusions.append("--exclude={}".format(argument))


# Do the actual backup
logging.info("Starting rsync.")
if logfile and exclusions and args.quiet:
    rsync("-auhv", exclusions, "--log-file={}".format(logfile), backupdir, destinationdir)
elif logfile and exclusions:
    print(rsync("-auhv", exclusions, "--log-file={}".format(logfile), backupdir, destinationdir))
elif args.quiet and exclusions:
    rsync("-av", exclusions, backupdir, destinationdir)
elif logfile and args.quiet:
    rsync("-av", "--log-file={}".format(logfile), backupdir, destinationdir)
else:
    rsync("-av", backupdir, destinationdir)

logging.info("done.")