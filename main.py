import subprocess
import requests
import sys

print("""

CATSCOBOT-SOURCE

""")
while True:
  try:
    code = requests.get("https://raw.githubusercontent.com/ethandacat/catscobott/refs/heads/main/prod.py").text
    print("Version Number: "+code.split("#")[0].split("\n")[0])
    exec(code)
  except KeyboardInterrupt:
    print("byeeee~!")
    sys.exit()
  except BaseException as e:
    print("""

An error occured.

The program is sleeping for 5 seconds. Close the program if needed.
    """)
    time.sleep(5)
