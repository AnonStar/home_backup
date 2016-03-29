This is just a simple backup script i wrote together for myself, mainly to learn python. If I get around to improve it, maybe it will someday be actually useful for some other people except me.

Usage:
rsync_mail.py [-h] [-t] [-e EXCLUDE] [-l LOGFILE] [-q] [-m MAIL] [-u]
                     [-d] [-c CONFIG] [--delete] [--legacy] [--check]
                     [--link LINK]
                     SOURCE TARGET

positional arguments:
  SOURCE                Specify the directory to backup (SOURCE).
  TARGET                Specify the directory where the backup should be
                        stored (TARGET).

optional arguments:
  -h, --help            show this help message and exit
  -t, --trash           Delete unnecessary files and empty the trash.
  -e EXCLUDE, --exclude EXCLUDE
                        Exlude the following directories from backup.
  -l LOGFILE, --logfile LOGFILE
                        Specify the logfile to monitor.
  -q, --quiet           Do not print to stdout.
  -m MAIL, --mail MAIL  eMail-Adress whereto send the rsync-log to. Use this
                        with the --config option to provide a Properties-File
                        with the SMTP-Server-Config.
  -u, --update          Keeps files in destination if they are more recent.
  -d, --debug           Generates a detailed rsync log.
  -c CONFIG, --config CONFIG
                        Loads the config from property file.
  --delete              Deletes files and folders in the backup which has been
                        deleted in the source.
  --legacy              Support for some systems without the ability to change
                        permissions
  --check               Checks the backup byte-by-byte. This can take a while.
                        This option verifies that a backup is fully identical
                        with the source.
  --link LINK           Creates a new Backup and only saves differences to the
                        specified main-backup. For an incremental backup use
                        this option with the parameter ->last<-. You can use
                        the parameter ->date<- as the Destination to create a
                        new Folder with todays date on the same level as the
                        specified main-backup.


Changelog:

02/15: Pascal Laub: improved the script, added a mail-option.

-Sebastian Gumprich http://zufallsheld.de
-Pascal Laub
