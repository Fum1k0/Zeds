#!/usr/bin/python2

# Program : zeds.py
# Ver     : 0.01a

# USED AT YOUR OWN RISK! I'M NOT RESPONSIBLE FOR YOURS ACTS

import os         # Process info
import getpass    #    User info
import platform   #      OS info
import biplist    #    Conf info

from time import gmtime, strftime

_sCurrentOS      = platform.system() + ' ' + platform.release() 
_sCurrentTime    = strftime("%Y-%m-%d %H:%M:%S", gmtime())
_sCurrentVersion = "0.01a"
_sCurrentYear    = "2014"
_sCurrentUser    = getpass.getuser()

_lSafeHosts = ['#','127.0.0.1localhost','255.255.255.255broadcasthost','::1localhost','fe80::1%lo0localhost']

def init():
  print '>>> Zeds '   + _sCurrentVersion + ' -- ' + _sCurrentYear + ' <<<'
  print '    User : ' + _sCurrentUser
  print '    Time : ' + _sCurrentTime 
  print '      OS : ' + _sCurrentOS
  print ''

def hosts():
  with open('/etc/hosts','r') as fHosts:
    for sLine in fHosts:
      bWhiteList = False
      sArgs = sLine.strip();
      sArgs = sArgs.replace(' ','')
      sArgs = sArgs.replace('	','')
      for sRules in _lSafeHosts:
        if sRules in sArgs:
          bWhiteList = True
      if bWhiteList == False:
        print 'N0 - HOSTS: ' + sLine

def safari_start():
  f = biplist.readPlist("/Users/" + _sCurrentUser + "/Library/Preferences/com.apple.Safari.plist")
  print 'S0 - [LOVS] ' + f["LastOSVersionSafariWasLaunchedOn"]
  print 'S0 - [NLSV] ' + f["NewestLaunchedSafariVersion"]
  print 'S0 - [HOME] ' + f["HomePage"]

def safari_plugins():
  for f in os.listdir("/Library/Internet Plug-Ins/"):
    print 'S1 - ' + f

  for f in os.listdir("/Users/" + _sCurrentUser + "/Library/Safari/Extensions/"):
    if not 'Extensions.plist' in f:
      print 'S2 - ' + f

def main():
  init()
  hosts()
  safari_start()
  safari_plugins()


if __name__ == "__main__":
    main()