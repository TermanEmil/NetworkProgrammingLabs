import sys
import smtplib
import optparse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def build_arg_options():
    option_parser = optparse.OptionParser()
    option_parser.add_option(
        '-e', '--email',
        dest='from_email',
        help='Email to send from')

    option_parser.add_option(
        '-p', '--password',
        dest='password',
        help='Password for the email to send from')

    option_parser.add_option(
        '--to',
        dest='to_email',
        help='The email to send to')

    option_parser.add_option(
        '-s', '--subject',
        dest='subject',
        default='Smtplib mail test',
        help="The email's subject")

    option_parser.add_option(
        '-b', '--body',
        dest='body',
        default='',
        help="The email's body")

    option_parser.add_option(
        '--attachment',
        dest='attachment',
        help="The email's attachment, if needed")

    return option_parser


def get_app_options(option_parser):
    options, args = option_parser.parse_args()

    if options.from_email is None:
        raise Exception('No from email provided')

    if options.password is None:
        raise Exception('No password provided')

    if options.to_email is None:
        raise Exception('No destination email provided')

    return options


def build_attachment(attachment_filename):
    attachment = open(attachment_filename, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header(
        'Content-Disposition', "attachment; filename= %s" % attachment_filename)

    return p


def build_msg(from_mail, to_mail, subject, body, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = from_mail
    msg['To'] = to_mail
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    if attachment is not None:
        msg.attach(build_attachment(attachment))

    return msg.as_string()


def send_email(app_options):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()

    server.login(app_options.from_email, app_options.password)

    msg = build_msg(
        app_options.from_email,
        app_options.to_email,
        app_options.subject,
        app_options.body,
        app_options.attachment)

    server.sendmail(
        app_options.from_email,
        app_options.to_email,
        msg)

    server.close()
    print('Email sent!')


if __name__ == '__main__':
    try:
        app_options = get_app_options(build_arg_options())
        send_email(app_options)
    except Exception as e:
        print('[Failed]: ' + str(e))
        sys.exit(-1)
