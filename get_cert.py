import socket
import ssl
domain = "www.concordia.ca"
def get_certificate(hostname):
    #creates a wrapper that makes a scoket like object that can encrypt and decrypt ssl dat
    #allows acces to scoket method getpeercert(), which returns a dict of the certificate
    context = ssl.create_default_context()
    ssl_socket = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname,)
    ssl_socket.connect((hostname, 443))
    certificate_info = ssl_socket.getpeercert()
    return certificate_info

if __name__ == '__main__':
    print(get_certificate(domain))
