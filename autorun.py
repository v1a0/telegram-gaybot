import subprocess
import sys

while True:
    process = subprocess.Popen([sys.executable, "bot.py"])
    process.wait()
