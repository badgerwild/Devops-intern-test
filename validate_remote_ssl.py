from paramiko import SSHClient, sftp_client
from validate_local_ssl import evaluate_expiration, get_date_difference
from config import REMOTE_HOST, USERNAME,REMOTE_DIR_PATH, REMOTE_SCRIPT_PATH

def path_exists(stfp, path):
    '''validates that a remote file exists, takes if a stfp object and a directory path on the remote server'''
    try:
        stfp.stat(path)
        return 1
    except FileNotFoundError:
        return 0
#intitialize a SSH client and have it connect to the server

client = SSHClient()
client.load_system_host_keys()
try:
    client.connect(hostname=REMOTE_HOST, username=USERNAME)
except:
    print('could not connect, either credentials are incorrect or rsa key is not set up for this system')
    exit(0)
#creates a secure file transfer protocal(sftp) object for the SSH object
remote_actor = client.open_sftp()
#checks to see if remote path exists, if not it creates it:
if path_exists(remote_actor, REMOTE_DIR_PATH) != 1:
    remote_actor.mkdir(REMOTE_DIR_PATH)
#checks if remote script exist, if the script already exists on remote server it is deleted
if path_exists(remote_actor, REMOTE_SCRIPT_PATH) == 1:
    remote_actor.remove(REMOTE_SCRIPT_PATH)
#copies the script get_ceet script to remote server, stdout is set up so when script is run it will
#return a dictionary ofbject pf the script back to the local machine where it can be evaluated. 
remote_actor.put('/home/jason/SAP-Devops-intern-test/get_cert.py', REMOTE_SCRIPT_PATH)
stdin, stdout, stderr = client.exec_command('python3 ssl_script/get_cert.py')
output_certificate = stdout.channel.recv(1024).decode("UTF-8")
client.close()
try:
    evaluate_expiration(get_date_difference(output_certificate))
except:
    print('Certificate could not be found on the server, please recheck credentials')
