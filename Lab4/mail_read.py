import sys
import poplib


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

    for line in body:
        print(line.decode('utf-8'))

    server.quit()
