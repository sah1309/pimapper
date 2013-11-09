import subprocess
import re

cmd = 'arping -c 1 ' + '172.16.10.101'     

p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)                               
output, errors = p.communicate()                                                            
if output is not None :                                                                     
  mac = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', output, re.I).group()
  print mac
