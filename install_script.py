import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'bs4'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'ttkthemes'])

# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tkinter'])
# subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PIL'])