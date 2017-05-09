import smtplib
import email
import sys
import getpass
from email.mime.text import MIMEText

"""
"""

# Mail sender class. Not receiving shit for now, but smtp_custom.py is server. Tweak \o/
class mail_send(object):

    # Initializer for the class. This is where the username etc should be checked.
    def __init__(self, msg):
        self.msg = MIMEText(msg) 

    # Adds the info needed for the mail before sending it.
    def add_recipients(self, subject):
        self.msg['To'] = email.utils.formataddr(('Recipient', self.receiver))
        self.msg['From'] = email.utils.formataddr(('Author', self.sender))
        self.msg['Subject'] = subject
        print self.msg["Subject"]

    # Checks credentials for the user. If sender is not defined (hardcoded) it will be prompted.
    def check_credentials(self, receiver):
        # Change here
        self.sender = ""
        self.receiver = receiver
        print "Sending from %s to %s" % (self.sender, self.receiver)

        if not self.receiver:
            print "No receiver address: %s" % self.receiver
            exit()

        self.password = getpass.getpass("Input password for %s: " % self.sender)

    # This is where the magic happens lmao.
    def run_server(self):
        target = "smtp.live.com"
        target_port = 587

        print self.sender
        print "Connecting to %s:%d" % (target, target_port)
        server = smtplib.SMTP(target, target_port, timeout=5)

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
        except smtplib.SMTPServerDisconnected as e:
            print "Error: %s" % e
            server.quit()

        print "Mail sent to %s" % self.receiver


if __name__ == "__main__":
    sender = mail_send("HELLO")
    sender.check_credentials("")
    sender.add_recipients("HELLO THIS IS TEST")
    sender.run_server()
