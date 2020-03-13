'''this script evaluates the validity of the ssl certificate on the local  server'''
import datetime
import socket
import ssl
import calendar
import sys
from termcolor import colored
from config import DOMAIN_TO_CHECK

def get_certificate(hostname):
    #creates a wrapper that makes a scoket like object that can encrypt and decrypt ssl dat
    #allows acces to scoket method getpeercert(), which returns a dict of the certificate
    context = ssl.create_default_context()
    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname,)
    ssl_socket.connect((hostname, 443))
    certificate_info = ssl_socket.getpeercert()
    return certificate_info


def get_date_difference(certificate):
    '''returns a dict containing the difference between certificate date and the current date, and
    the expiration date'''
    if 'notAfter' in certificate:
        date = certificate['notAfter']
    else:
        print('certificate object is incorrect format or does not exist')
        sys.exit(1)
    split_date = date.split()
    #converts the abreviation of the month into an int, so it can be made into a date time object
    month_to_number = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    cert_month = month_to_number[split_date[0]]
    #creates datetime object out of the date returned by the certificate
    cert_day = datetime.date(int(split_date[3]), int(cert_month), int(split_date[1]))
    today = datetime.date.today()
    return[(cert_day-today).days, date]
    #return cert_day


def evaluate_expiration(dates):
    '''prints the expiration date, and then a colored warning depending on time to expire'''
    print('The certificate is valid until: ' + dates[1])
    if dates[0] < 15:
        print(colored('CRITICAL', 'red'))
    elif dates[0] >= 15 and dates[0] < 30:
        print(colored('WARNING', 'yellow'))
    elif dates[0] >= 30:
        print(colored('INFO', 'green'))


if __name__ == '__main__':
    evaluate_expiration(get_date_difference(get_certificate(DOMAIN_TO_CHECK)))
