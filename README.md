This is a backup-script written in python using rsync. It is tested on Ubuntu 14.04 and Arch Linux (using --legacy).
It can backup incremental and differential. It will send you an email and summarize the backup.

NOTE: This is NOT a recommendet programming practice and it's definetly not optimal. While getting more weight it bothers me, that I hadn't did it optimal from the beginning. Maybe I will refactor it, we will see ;)
But it's working quite good.

Usage:

rsync_mail.py [-h] [-t] [-e EXCLUDE] [-l LOGFILE] [-q] [-m MAIL] [-u]
                     [-d] [-c CONFIG] [--delete] [--legacy] [--check]
                     [--link LINK] [--date]
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
                        
  --check               Checks the transfered files byte-by-byte with a
                        generated checksum. This can take a while. This option
                        verifies that a backup is fully identical with the
                        source.
                        
  --link LINK           Creates a new Backup and only saves differences to the
                        specified main-backup. For an incremental backup use
                        this option with the argument ->last<-. The script
                        then looksup the last backup in the target directory.
                        
  --date                Saves the backup into a subfolder named after the
                        actual date in format yyyy-MM-dd into the target
                        directory.


Changelog:

03/15: Pascal Laub: improved the script, added some options including incremental and differential backups.

-Sebastian Gumprich http://zufallsheld.de
-Pascal Laub
