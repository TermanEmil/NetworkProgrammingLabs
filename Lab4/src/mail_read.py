import sys
import poplib
import email


def get_mails_body(msg):
    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            # skip any text/plain (txt) attachments
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = msg.get_payload(decode=True)

    return body.decode('utf-8')


def print_mail_headers(msg):
    for kv in msg._headers:
        print('%s: %s' % (kv[0], kv[1]))


def pretty_print_email(msg):
    print("Subject: %s" % msg['Subject'])
    print("From: %s" % msg['From'])
    print("To: %s" % msg['To'])
    print("Body: %s" % get_mails_body(msg))

    print()
    print("Headers: ----------------------------------------------------------")
    print_mail_headers(msg)


if __name__ == '__main__':
    server = poplib.POP3_SSL('pop.googlemail.com', '995')
    server.user('devemail42@gmail.com')
    server.pass_("%Is9R~lvJ5'ljOU{0wg?")

    try:
        _, items, _ = server.list()
        mail = items[0]
    except:
        print('[Failed]: No unseen messages')
        sys.exit(-1)

    id, size = str.split(mail.decode('utf-8'))
    resp, body, octets = server.retr(id)

    server.quit()

    raw_email = b"\n".join(body)
    parsed_email = email.message_from_bytes(raw_email)

    pretty_print_email(parsed_email)

