#!/usr/bin/python2

# Program : zeds.py
#    MOTD : I like trains ! :)

# I'M NOT RESPONSIBLE FOR YOURS ACTS

# R0 -> Startup Items 
# L0 -> Agents
# L1 -> Daemons
# H0 -> Hosts
# S0 -> Safari conf
# S1 -> Safari Plugins
# S2 -> Safari Extensions

import os         # Process info
import getpass    #    User info
import platform   #      OS info
import biplist    #    Conf info
import subprocess #  Update info

from time import gmtime, strftime

_sAuthor         = "Ikes"
_sCurrentOS      = platform.system() + ' ' + platform.mac_ver()[0]
_sCurrentTime    = strftime("%Y-%m-%d %H:%M:%S", gmtime())
_sCurrentVersion = "0.5"
_sCurrentYear    = "2015"
_sCurrentUser    = getpass.getuser()

_lSafeHosts         = []
_lSafeSystemAgents  = []
_lSafeSystemDaemons = []
_lSafeUserBin       = []
_lSafeUsersShared   = []

def darwin():
  if not 'Darwin' in _sCurrentOS:
    print 'ERROR - MacOSX Only...' # Oh boy !
    exit(1)

def conf():
  try:
    with open('db.cfg') as f:
      content = f.readlines()
    
    state = 0
    for value in content:
      value = value.strip('\t\n\r')
      if '[SafeHosts]' in value:
        state = 1
      elif state == 1 and len(value) > 1:
        _lSafeHosts.append(value)
      elif state == 1 and len(value) == 0:
        state = 0
      elif '[SafeSystemAgents]' in value:
        state = 2
      elif state == 2 and len(value) > 1:
        _lSafeSystemAgents.append(value)
      elif state == 2 and len(value) == 0:
        state = 0
      elif '[SafeSystemDaemons]' in value:
        state = 3
      elif state == 3 and len(value) > 1:
        _lSafeSystemDaemons.append(value)
      elif state == 3 and len(value) == 0:
        state = 0
      elif '[SafeUserBin]' in value:
        state = 4
      elif state == 4 and len(value) > 1:
        _lSafeUserBin.append(value)
      elif state == 4 and len(value) == 0:
        state = 0
      elif '[SafeUsersShared]' in value:
        state = 5
      elif state == 5 and len(value) > 1:
        _lSafeUsersShared.append(value)
      elif state == 5 and len(value) == 1:
        state = 0
  except:
  	 print 'ERROR - Conf file not found'

def init():
  print '>>> Zeds '   + _sCurrentVersion + ' -- ' + _sCurrentYear + ' <<<'
  print '>>> Author : ' + _sAuthor + '\n'

  print '    User : ' + _sCurrentUser
  print '    Time : ' + _sCurrentTime 
  print '      OS : ' + _sCurrentOS
  print '    Arch : ' + platform.mac_ver()[2]
  print ''

def update():
  bFound = False
  pProc = subprocess.Popen(['softwareupdate','-l'],
  	stdin = subprocess.PIPE,
  	stdout = subprocess.PIPE,
  	stderr = subprocess.PIPE
  	)
  (out, err) = pProc.communicate()
  sIsUpToDate =  out + err
  if "No new software available" in sIsUpToDate:
    bFound = True
  if bFound == False:
    print 'U0 - Update(s) Available(s)' 

def hosts():
  with open('/etc/hosts','r') as fHosts:
    for sLine in fHosts:
      bWhiteList = False
      sArgs = sLine.strip();
      sArgs = sArgs.replace(' ','')
      sArgs = sArgs.replace('	','')
      for sRules in _lSafeHosts:
        if sRules in sArgs or sLine[0] == '#':
          bWhiteList = True
      if bWhiteList == False:
        print 'N0 - HOSTS: ' + sLine


def startup_item():
  for f in os.listdir('/Library/StartupItems/'):
    print 'R0 - [/Library/StartupItems] ' + f

def agents():
  # Administrator Agents
  for f in os.listdir('/Library/LaunchAgents/'):
    print 'A0 - [/Library/LaunchAgents] ' + f
    
  # Launch Agents
  for f in os.listdir("/Users/" + _sCurrentUser + "/Library/LaunchAgents/"):
    print 'A1 - [~/Library/LaunchAgents] ' + f

  # System Agents  
  for f in os.listdir('/System/Library/LaunchAgents/'):
    bFound = False
    for sWhiteList in _lSafeSystemAgents:
      if sWhiteList in f:
        bFound = True	
    if bFound == False:
      print 'A2 - [/System/Library/LaunchAgents] ' + f

def daemons():
  # Administrator Deamons
  for f in os.listdir('/Library/LaunchDaemons/'):
    print 'D0 - [/Library/LaunchDaemons] ' + f

  # System Agents  
  for f in os.listdir('/System/Library/LaunchDaemons/'):
    bFound = False
    for sWhiteList in _lSafeSystemDaemons:
      if sWhiteList in f:
        bFound = True	
    if bFound == False:
      print 'D1 - [/System/Library/LaunchDaemons] ' + f

def apps():
  for f in os.listdir("/Applications/"):
    if not '.DS_Store' in f and not '.localized' in f:
      if 'MacD' in f or 'MacPr' in f or 'Mac D' in f or 'MacSw' in f or 'Mac P' in f:
        print 'A1 - [Applications] ' + f + ' <- SUSPICIOUS'
      else:
        print 'A0 - [Applications] ' + f

def library():
  for f in os.listdir("/Library/"):
    if not '.DS_Store' in f and not '.localized' in f:
      print 'L0 - [Library] ' + f

  for f in os.listdir("/Library/Application Support/"):
    if not '.DS_Store' in f and not '.localized' in f:
      print 'A1 - [/Library/Application Support/] ' + f

def bin():
  for f in os.listdir("/usr/bin/"):
    bFound = False
    for sWhiteList in _lSafeUserBin:
      if sWhiteList == f:
        bFound = True
    if bFound == False:
      print 'B0 - [/usr/bin] ' + f

  for f in os.listdir("/usr/local/bin"):
    print 'B1 - [/usr/local/bin] ' + f  

def shared():
  for f in os.listdir("/Users/Shared/"):
    bFound = False
    for sWhiteList in _lSafeUsersShared:
      if sWhiteList in f:
        bFound = True	
    if bFound == False:
      print 'O1 - [/Users/Shared/] ' + f 

def safari_start():
  f = biplist.readPlist("/Users/" + _sCurrentUser + "/Library/Preferences/com.apple.Safari.plist")
  print 'S0 - [LastOSVersionSafariWasLaunchedOn] ' + f["LastOSVersionSafariWasLaunchedOn"]
  print 'S0 - [NewestLaunchedSafariVersion] ' + f["NewestLaunchedSafariVersion"]
  print 'S0 - [HomePage] ' + f["HomePage"]

def safari_plugins():
  for f in os.listdir("/Library/Internet Plug-Ins/"):
    print 'S1 - [/Library/Internet Plug-Ins] ' + f

  for f in os.listdir("/Users/" + _sCurrentUser + "/Library/Safari/Extensions/"):
    if not 'Extensions.plist' in f:
      print 'S2 - [~/Library/Safari/Extensions/] ' + f

def main():
  darwin()
  conf()
  init()
  # update()
  print '-----------------------------------------------------------------------'
  startup_item()
  print '-----------------------------------------------------------------------'
  agents()
  print '-----------------------------------------------------------------------'
  daemons()
  print '-----------------------------------------------------------------------'
  library()
  print '-----------------------------------------------------------------------'
  apps()
  print '-----------------------------------------------------------------------'
  bin()
  print '-----------------------------------------------------------------------'
  shared()
  print '-----------------------------------------------------------------------'
  safari_start()
  safari_plugins()
  print '-----------------------------------------------------------------------'
  hosts()


if __name__ == "__main__":
  main()