import smtplib
import email
import sys
import getpass
from email.mime.text import MIMEText

"""
Fill in the blanks to make it work :) 
Currently running under the hotmail domain (smtp.live.com:587). 
Can be changed under run_server().

Mail changes are done under add_receipients.
"""

# Mail sender class. Not receiving shit for now, but smtp_custom.py is server. Tweak \o/
class mail_send(object):

    # Initializer for the class. This is where the username etc should be checked.
    def __init__(self):
        self.sender = ""
        self.receiver = ""
        self.msg = MIMEText('This is the body of test message.')

    # Adds the info needed for the mail before sending it.
    def add_recipients(self):
        self.msg['To'] = email.utils.formataddr(('Recipient', self.receiver))
        self.msg['From'] = email.utils.formataddr(('Author', self.sender))
        self.msg['Subject'] = 'Hello im sending a mail to test this thingy'

    # Checks credentials for the user. If sender is not defined (hardcoded) it will be prompted.
    def check_credentials(self):
        self.sender = raw_input("Sender mail: ") if not self.sender else 0 
        self.receiver= raw_input("Receiver mail: ") if not self.receiver else 0 
        self.password = getpass.getpass("Password: ")

    # This is where the magic happens lmao.
    def run_server(self):
        target = "smtp.live.com"
        target_port = 587
        print "Connecting to %s:%d" % (target, target_port)
        server = smtplib.SMTP(target, target_port)

        # Remove # to enable commenting
        #server.set_debuglevel(True) 

        server.ehlo()
        print "Setting up TLS" 
        server.starttls()
        server.ehlo()
    
        # Checks if the credentials work.
        try:
            print "Trying to log in.."
            server.login(self.sender, self.password)
            print "Logged in as %s" % self.sender
        except smtplib.SMTPAuthenticationError:
            print "Bad username or password" 
            try:
                print "Quitting server"
                server.quit()
            except smtplib.SMTPServerDisconnected:
                print "Quitting program"
                sys.exit()

        try:
            server.sendmail(self.sender, self.receiver, self.msg.as_string())
        finally:
            print "Mail sent to %s" % self.receiver
            server.quit()


if __name__ == "__main__":
    sender = mail_send()
    sender.check_credentials()
    sender.add_recipients()
    sender.run_server()
