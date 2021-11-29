"""
For installing required modules in download.py, new modules is added by their name 
in the required array

@author : Simon

"""

import sys
import subprocess

required = {'requests','pandas','PyPDF2'}

for req in required:
    subprocess.check_call([sys.executable, "-m", "pip", "install", req])