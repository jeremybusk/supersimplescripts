#!/usr/bin/env python3
#auto reply email bot for Microsoft 365.
#Is a good reference of a lot of basic imap commands and functions.
#Haven't tested this after revision so you may have to do some tweeking.
#It should be pretty close those. I'll try and clean it up soon.
import imaplib
import sys
import time
import re
import smtplib
import email
from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

imap_port = 995
imap_host = 'outlook.office365.com'
imap_user = 'youremail@your365domain.com'
imap_pass = 'yourpassword'
smtp_port = 587
smtp_server = 'smtp.office365.com'
smtp_user = imap_user
smtp_pass = imap_pass


def main():
    get_email()


def get_email():
    imap_port = 993
    imap_host = 'outlook.office365.com'
    imap_user = 'youremail@your365domain.com'
    imap_pass = 'yourpassword'
    regex_case_id = re.compile('<ID>(.*?)</ID>')
    regex_ipaddr = re.compile('<IP_Address>(.*?)</IP_Address>')
    regex_contact_email = re.compile('<Email>(.*?)</Email>')
    regex_contact_name = re.compile('<Name>(.*?)</Name>')
    M = imaplib.IMAP4_SSL(imap_host, imap_port)
    try:
        (retcode, capabilities) = M.login(imap_user, imap_pass)
    except:
        print(sys.exc_info()[1])
        sys.exit(1)
    M.select(mailbox='Inbox', readonly=True)
    typ, msgnums = M.search(None, '(BODY "</Case>" BODY "<Case>" BODY "</Some other word to match>")')
    if retcode == 'OK':
        for num in msgnums[0].split():
            #fetch message by message number
            typ, data = M.fetch(num, '(RFC822)')
            msg_obj = email.message_from_bytes(data[0][1])
            #Above returns a message object structure from a byte string.
            #This is exactly equivalent to BytesParser().parsebytes(s)
            for part in msg_obj.walk():
                mtype = part.get_content_type()
                if mtype == 'application/xml':
                    xml = part.get_payload(decode=True)
                    xml_string = xml.decode('utf-8')
                    string_with_xml = xml_string
                elif mtype == 'text/plain':
                    string_with_xml = part.get_payload(decode=True).decode('utf-8')
                elif mtype == 'text/html':
                    string_with_xml = part.get_payload(decode=True).decode('utf-8')
                else:
                    pass
            m = regex_case_id.search(string_with_xml)
            if m:
                ipaddr = m.group(1)
            m = regex_contact_email.search(string_with_xml)
            if m:
                contact_email = m.group(1)
            m = regex_entity_name.search(string_with_xml)
            if m:
                contact_name = m.group(1)
            body = create_email_response_text(contact_email, contact_name, string_with_xml)
            result = send_email(body)
            if result:
                #move message to completed forward after successful send
                msg_uid = num
                result = M.uid('COPY', msg_uid, 'RepliedToEmails')
                print('moving')
                print(result)
                time.sleep(5)
                if result[0] == 'OK':
                    mov, data = M.uid('STORE', msg_uid , '+FLAGS', '(\Deleted)')
                    M.expunge()
    M.close()
def create_email_response_text(contact_email, contact_name, xml):
    #The xml/notice is also attached to this response.
    response_body = '''
Dear {},
Thanks for emailing me for id, blah blah blah, response...
Thanks,
{}

------------------------------------------
{}

    '''.format(contact_name, reply_name, xml)
    return response_body
def send_email(body):
    smtp_host = 'smtp.office365.com'
    smtp_port = 587
    smtp_user = 'youremailrelay@yourrelaydomain.com'
    smtp_pass = 'yourrelaypassword'
    to_email = 'destination.email@yourdomain.com'
    #from_email = 'dispatcher.email@veracitynetworks.com'
    from_email = 'noreply@veracitynetworks.com'
    try:
        msg = MIMEMultipart()
        msg['From'] = 'noreply'
        msg['To'] = to_email
        msg['Subject'] = "Reponse Subject"
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        print(text)
        s = smtplib.SMTP(smtp_host, smtp_port)
        s.ehlo()
        s.starttls()
        s.login(smtp_user, smtp_pass)
        s.sendmail(from_email, to_email, text)
        s.quit()
        return True
    except:
        return False
if __name__ == '__main__':
    main()
