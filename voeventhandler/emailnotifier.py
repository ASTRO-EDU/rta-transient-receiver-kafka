from email.message import EmailMessage
import smtplib
import json

class EmailNotifier(object):

    def __init__(self):
        f = open('voeventhandler/config/config.json')
        config = json.load(f)
        self.mail = Mail(config["sender_email"], config["sender_email_password"])
        self.to = config["email_recivers"]
        self.packet_with_email_notification = config["packet_with_email_notification"]
        self.important_email_subject = config["important_email_subject"]

    def sendEmails(self, voeventdata, result_row):
        
        if voeventdata.packet_type in self.packet_with_email_notification or voeventdata.is_ste: #it will send an email for GW, Neutrino event or STE events
            subject = f'Notice alert for {voeventdata.name}'
            body = f'The platform received a notice for the {voeventdata.name} event at {voeventdata.UTC} for triggerID {voeventdata.trigger_id}'
            if self.is_important(voeventdata):
                subject = self.important_email_subject + " " + subject
            self.mail.send_email(self.to, subject, body)
        
        #check if there are correlated instruments and send an email if so
        if result_row:
            subject = f'Correlations for {voeventdata.name}'
            body = f'The platform received a notice for the {voeventdata.name} at {voeventdata.UTC} for triggerID {voeventdata.trigger_id} with the following correlated events: {str(result_row)}'
            self.mail.send_email(self.to, subject, body)
    
    def is_important(self, voeventdata) -> bool:
        return False

class Mail():
    
    def __init__(self, gmail_user, gmail_password) -> None:
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
    
    def send_email(self, to, subject, body):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.gmail_user
        msg['To'] = ', '.join(to)
    
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(self.gmail_user, self.gmail_password)
            smtp_server.send_message(msg)
            smtp_server.close()
            print("Email sent successfully!")
        except Exception as ex:
            print("Something went wrong….",ex)