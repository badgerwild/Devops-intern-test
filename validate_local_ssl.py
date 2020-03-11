import datetime
import socket
import ssl
import calendar

domain = "www.amazon.com"

def get_certificate_date(hostname):
    context = ssl.create_default_context()
    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname,)
    ssl_socket.connect((hostname, 443))
    certificate_info = ssl_socket.getpeercert()

    if 'notAfter' in certificate_info:
        date = certificate_info['notAfter']
    split_date = date.split()
    month_to_number = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    cert_month = month_to_number[split_date[0]];
    cert_day = datetime.date(int(split_date[3]), int(cert_month), int(split_date[1]))
    return cert_day


if __name__ == '__main__':
    the_date = get_certificate_date(domain)
    print(the_date)
    print(datetime.date.today())
