This is a backup-script written in python using rsync. It is tested on Ubuntu 14.04 and Arch Linux (using --legacy). It can backup incremental and differential. It will send you an email and summarize the backup.

Usage:

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
                        
  --convert CONVERT     Converts filenames into another format if you are
                        transferring umlauts. E.g. --convert utf8
                        
  --backup              Saves the changed and deleted files into the .backup
                        folder.
                        
  --ssh                 In order to backup to another computer over ssh. Do
                        not use this with --legacy. Place your ssh-key on the
                        target machine in order to let rsync connect without a
                        password or use --private_key. Use this with target-
                        pattern: user@machine:/target/dir.
                        
  --private_key PRIVATE_KEY
                        If you wanto to backup to an external machine using
                        --ssh you may send your private keyfile for
                        authentication. Use this option with the absolute path
                        to your keyfile.
                        


Changelog:

02/15: Pascal Laub: improved the script, added a mail-option.

-Sebastian Gumprich http://zufallsheld.de
-Pascal Laub
