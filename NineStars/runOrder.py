__author__ = 'Administrator'
""" This modules use ssh tools
to connect remote server and exec some commands.
"""
import paramiko
import socket
import logging
import sys
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('E:\NineStars\NineStars\server.conf')

log_file = parser.get("log", "log_path")
log_format = "%(asctime)s - %(levelname)s: %(message)s"

class Order(object):
    """ some order to remote execute """

    def __init__(self, ip_add, sshTag, cmd=None):
        self.sshTag = sshTag
        self.ip_add = ip_add
        self.cmd = cmd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            logging.basicConfig(filename=log_file,
                                level=logging.ERROR,
                                format=log_format)
        except IOError:
            print "Please check your configure file for log path"
            sys.exit()
        self.user = parser.get(self.sshTag, "user")
        try:
            self.port = int(parser.get(self.sshTag, "port"))
        except ValueError:
            print "Please check your configure file and the port must be number type"
            sys.exit()
        self.password = parser.get(self.sshTag, "password")
        self.p_or_key = parser.get(self.sshTag, "p_or_key")
        self.output = 1
        self.errput = 1


    def ssh_connect(self, Uname):
        """ssh function"""
        try:
            if self.password.upper() == "YES":
                self.ssh.connect(self.ip_add, self.port, self.user, self.p_or_key)
            elif self.password.upper() == "NO":
                self.ssh.connect(self.ip_add, self.port, self.user, key_filename=self.p_or_key)
            else:
                print "please check your configure file for password option"
                sys.exit()
        except socket.error:
            print "please check your connection"
        except IOError:
            print "please check your key file path"
        except paramiko.SSHException:
            print "Authentication incorrect"
        else:
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command(self.cmd)
            self.out_log = self.stdout.readlines()
            self.err_log = self.stderr.readlines()
            if self.out_log:
                self.output = self.out_log
                #print self.output
                logging.error(Uname + " | exec command | " + self.cmd)
                logging.shutdown()
                return self.output
            elif self.err_log:
                self.errput = self.err_log
                #print self.errput
                logging.error(self.errput)
                logging.shutdown()
                return self.errput
        finally:
            #print "--------------------"
            self.ssh.close()

    def ssh_sftp(self, lfile, rfile):
        """ssh transfer files"""
        self.lfile = lfile
        self.rfile = rfile
        try:
            if self.password.upper() == "YES":
                self.ip_port = paramiko.Transport((self.ip_add, self.port))
                self.ip_port.connect(username=self.user, password=self.p_or_key)
            elif self.password.upper() == "NO":
                self.ip_port = paramiko.Transport((self.ip_add, self.port))
                #transfer the rsa format key
                self.t_key = paramiko.RSAKey.from_private_key_file(self.p_or_key)
                self.ip_port.connect(username=self.user, pkey=self.t_key)
            else:
                print "please check your configure file for password option"
                sys.exit()
        except socket.error:
            print "please check your connection"
        except IOError:
            print "please check your key file path"
        except paramiko.SSHException:
            print "Authentication incorrect"
        else:
            self.sftp = paramiko.SFTPClient.from_transport(self.ip_port)
            #self.remote_path = "/tmp/mytest"
            #self.local_path = r"./mytest"
            self.remote_path = self.rfile
            self.local_path = self.lfile            
            self.sftp.put(self.local_path, self.remote_path)
        finally:
            self.ip_port.close()


