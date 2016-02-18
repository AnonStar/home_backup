#!/usr/bin/env python
# coding: utf8

import os
import argparse
import logging
import subprocess
import ConfigParser
from shutil import rmtree
from email.mime.text import MIMEText
#from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP                    # use this for standard SMTP protocol (TLS encryption)
from email.MIMEText import MIMEText

class RsyncMail():
  """
  This script will backup files and folders via rsync with common arguments.
  A logfile and a mail can be specified to be informed about the backup result.
  In order to use the mail option SMTP-informations have to be specified.
  You can either do this by editing the load_SMTP_standards function
  or by handing over a standard property file with a SMTPSection and the 
  following parameters:
  
    server.mail:      Mail-Adress of the sender, e.g. my@mail.com
    server.adress:    The hostname of the SMTP-server, e.g. localhost or smtp.mail.com
    server.user:      The username for logging in
    server.password:  The users password (unencrypted)
    server.port:      The SMTP-Port
      
  The connection to the mail server will be encrypted with TLS.
  If you want to use SSL you have to uncomment the line
  
    #from smtplib import SMTP_SSL as SMTP
  
  and comment the line
  
    from smtplib import SMTP
  
  in the import-section.
  
  In order to use encrypted passwords you have to implement a service.
  You could use yagmail to do this. For more information regarding this topic
  read these:
  
  http://stackoverflow.com/questions/31827094/how-to-use-encrypted-password-in-python-email
  
  https://github.com/kootenpv/yagmail   
  """
  
  def load_SMTP_standards(self):
    self.serverAdress = 'sender@anonstar.org'
    self.SMTPServer = 'anonstar.org'
    self.SMTPUser = 'sender@anonstar.org'
    self.SMTPPassword = 'MailSender!90'
    self.SMTPPort = 25  
    
  def parse_args(self):

    #Parse arguments
    parser = argparse.ArgumentParser(
        description=__doc__)

    parser.add_argument("BACKUPDIR", help="Specify the directory to backup.")
    parser.add_argument("DESTINATIONDIR", help="Specify the directory where the backup is stored.")
    parser.add_argument("-t", "--trash", help="Delete unnecessary files and empty the trash.", action="store_true")
    parser.add_argument("-e", "--exclude", help="Exlude the following directories from backup.", action="append")
    parser.add_argument("-l", "--logfile", help="Specify the logfile to monitor.")
    parser.add_argument("-q", "--quiet", help="Do not print to stdout.", action="store_true")
    parser.add_argument("-m", "--mail", help="eMail-Adress whereto send the rsync-log to.")
    parser.add_argument("-u", "--update", help="Keeps files in destination if they are more recent.", action="store_true")
    parser.add_argument("-d", "--debug", help="Generates a detailed rsync log.", action="store_true")
    parser.add_argument("-s", "--smtp", help="Loads the SMTP-Config from property file.")
    parser.add_argument("--legacy", help="Support for some systems without the ability to change permissions", action="store_true")

    args = parser.parse_args()

    # Define variables
    self.backupdir = args.BACKUPDIR
    self.destinationdir = args.DESTINATIONDIR
    self.logfile = args.logfile
    self.mail = args.mail
    self.update = args.update
    self.debug = args.debug
    self.rsync_params = ["rsync"]
    self.args = args
    self.logger = logging.getLogger("logger")

    #Logging
    FORMAT = '%(asctime)-15s (%(levelname)s): %(message)s'

    if self.logfile and self.mail:
      if self.check_dir_exist(self.logfile):
              os.remove(self.logfile)

      if not self.debug:
          logging.basicConfig(filename=self.logfile, filemode='w', level=logging.INFO, format=FORMAT, datefmt='%Y.%m.%d %H:%M:%S')
      else:
          logging.basicConfig(filename=self.logfile, filemode='w', level=logging.DEBUG, format=FORMAT, datefmt='%Y.%m.%d %H:%M:%S')
          
    if not self.args.quiet:
        consoleHandler = logging.StreamHandler()
        console_format = logging.Formatter(FORMAT)
        consoleHandler.setFormatter(console_format)
        consoleHandler.setLevel(logging.DEBUG) if self.debug else consoleHandler.setLevel(logging.INFO)
        self.logger.addHandler(consoleHandler)
         
  # directory exist-check
  def check_dir_exist(self, os_dir):
      if os.path.exists(os_dir): 
          self.logger.debug("{} exists.".format(os_dir))
          return True
      else:
          self.logger.warning("{} does not exist.".format(os_dir))
          return False

  # delete function
  def delete_files(self, ending, indirectory):
      for r, d, f in os.walk(indirectory):
          for files in f:
              if files.endswith("." + ending):
                  try:
                      os.remove(os.path.join(r, files))
                      self.logger.info("Deleting {}/{}".format(r, files))
                  except OSError:
                      self.logger.warning("Could not delete {}/{}".format(r, files))
                      pass


  # Delete actual files first
  def delete_temp(self):
      if self.args.trash:
          file_types = ["tmp", "bak", "dmp"]
          for file_type in file_types:
              delete_files(file_type, backupdir)
          # Empty trash can
          try:
              rmtree(os.path.expanduser("~/.local/share/Trash/files"))
          except OSError:
              self.logger.warning("Could not empty the trash or trash already empty.")
              pass

  def handle_exclusions(self):
      # handle exclusions 
      if self.args.exclude:
        for argument in self.args.exclude:
          self.rsync_params.append("--exclude={}".format(argument))
          
  # Assemble parameters
  def assemble_params(self):
      if not self.args.legacy:
        params="-ah"
      else: params="-rlth"
      params = params + "u" if self.update else params
      params = params + "v" if self.debug else params
      self.rsync_params.append(params)
      if self.logfile:
        self.rsync_params.append("--log-file=" + self.logfile)
      self.handle_exclusions()
      self.rsync_params.append(self.backupdir) 
      self.rsync_params.append(self.destinationdir)
      self.logger.debug(self.rsync_params)
      
  def load_SMTP_Server_Config(self, path):
    try:
      config = ConfigParser.RawConfigParser()
      config.read(path)
      self.serverAdress = config.get('SMTPSection', 'server.mail')
      self.SMTPServer = config.get('SMTPSection', 'server.adress')
      self.SMTPUser = config.get('SMTPSection', 'server.user')
      self.SMTPPassword = config.get('SMTPSection', 'server.password')
      self.SMTPPort = config.get('SMTPSection', 'server.port')
    except:
      self.mail = False
      self.logger.error("Couldn't load SMTP-Config. Skipping mail...")
       
  # Mail mit Log senden
  # Params: Recipient, Logfile, Returncode, Output
  def send_mail(self, recipient, logfile, return_value, output):
    # Load the SMTP Config from property file if existing
    if self.args.smtp and self.check_dir_exist(self.args.smtp):
      self.load_SMTP_Server_Config(self.args.smtp)
    else: 
      self.load_SMTP_standards()
    if self.mail:
      if logfile:
        # Open the logfile for reading.
        fp = open(self.logfile, 'rb')
        # Create a text/plain message
        msg = MIMEText(fp.read())
        fp.close()
      elif output:
        msg = MIMEText(output)
      else:
        msg = MIMEText("The Backup is done.")
      if return_value == 0:
        msg['Subject'] = 'The backup has completed successfully.'
      else:
        msg['Subject'] = "The backup couldn't succeed! An Error occured! ReturnCode=" + str(return_value)
      msg['From'] = self.serverAdress
      msg['To'] = recipient

      try:
          self.conn = SMTP(self.SMTPServer, self.SMTPPort)
          self.conn.set_debuglevel(False)
          # Starting an encrypted TLS-Session
          self.conn.starttls()
          self.conn.login(self.SMTPUser, self.SMTPPassword)
          self.conn.sendmail(self.serverAdress, [recipient], msg.as_string())
          self.logger.info("Successfully sent mail to %s" % recipient)
      except Exception as e:
          self.logger.error("Sending mail failed! Error: %s" % e)
      finally:
          self.conn.close()
 
  # Do the actual backup
  def main(self):
      self.parse_args()
      self.return_value = 0
      if not self.check_dir_exist(self.backupdir):
          self.logger.error("The Backup-Directory " + self.backupdir + " does not exist! Exiting...")
          if self.mail:
              self.send_mail(self.mail, self.logfile, 1, "The Backup-Directory " + self.backupdir + " does not exist! Exiting...")
          exit(1)
      self.assemble_params();
      if self.args.trash:
          self.delete_temp();
      if self.logfile: 
          self.logger.info("Saving logfile to " + self.logfile) 
      else: 
          self.logger.info("Starting rsync without a logfile.")              
      try:
          out = subprocess.check_output(self.rsync_params, stderr=subprocess.STDOUT, shell=False)
          self.logger.info(out)
      except subprocess.CalledProcessError as e:
          self.return_value = e.returncode
          self.logger.error("The command")
          self.logger.error(e.cmd)
          self.logger.error("exited with returnvalue " + str(self.return_value) + " and the following output:")
          self.logger.info(e.output)
          if self.mail:
              self.send_mail(self.mail, self.logfile, self.return_value, e.output)
          exit(1)
      self.logger.info("Backup done. Rsync exited with returncode " + str(self.return_value))
      if self.mail:
          self.send_mail(self.mail, self.logfile, self.return_value, out)

x = RsyncMail();
x.main();
