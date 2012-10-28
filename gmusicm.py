#! /usr/bin/env python

import argparse
import sys
import os
from gmusicapi.api import Api

VERSION     = "0.1"
DESCRIPTION =\
"""Upload/download music to/from Google Music"""

DEFAULT_DIR = './'

class QuietStream:
    def __init__(self): pass
    def write(self, data): pass
    def read(self, data): pass
    def flush(self): pass
    def close(self): pass

def configure():
    parser = argparse.ArgumentParser( description=DESCRIPTION )
    parser.add_argument( '-v', '--version', action='version',
                         version='%(prog)s ' + VERSION )
    parser.add_argument( '-q', '--quiet', action='store_true', default=False,
                         dest='doQuiet', help='Make quiet.' )
    parser.add_argument( '-u', '--email', action='store', dest='email',
                         help='Email of the Google Account.' )
    parser.add_argument( '-p', '--password', action='store', dest='password',
                         help='Password of the Google Account.' )
    parser.add_argument( 'action', choices=['download', 'upload'],
                         help='Action to do.' )
    parser.add_argument( 'directory', action='store', nargs='?',
                         default=DEFAULT_DIR, help='Set the source/destination '
                         + 'directory. Default to ' + DEFAULT_DIR )
    opt, _ = parser.parse_known_args()
    if opt.doQuiet == True:
        sys.stdout, sys.__stdout__ = QuietStream(), QuietStream()
    return opt

class Utils:
    @staticmethod
    def findMp3(directory):
        mp3List = []
        for root, dirs, files in os.walk(directory):
            for f in files:
                filename = os.path.join(root, f)
                if filename.endswith('.mp3'):
                    mp3List.append(filename)
        return mp3List


class GMusicM:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.api = Api()
        self.login()

    def __del__(self):
        self.logout()

    def login(self):
        print "Login"
        self.isLogin = self.api.login(self.email, self.password)
        if self.isLogin == False:
            print >> sys.stderr, "Can't login to Goole Music."

    def logout(self):
        print "Logout"
        self.api.logout()
        self.isLogin = False

    def upload(self, directory):
        if self.isLogin == False:
            return
        mp3List = Utils.findMp3(directory)
        print "Upload song"
        for filename in mp3List:
            print"\t- " + filename
            self.api.upload(filename)

    def download(self, directory):
        if self.isLogin == False:
            return

def main(opt):
    gMusicM = GMusicM(opt.email, opt.password)
    if opt.action == 'upload':
        gMusicM.upload(opt.directory)
    else:
        gMusicM.download(opt.directory)

if __name__ == "__main__":
  try:
    main(configure())
  except (KeyboardInterrupt, SystemExit):
      pass
  sys.exit(0)
