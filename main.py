import subprocess
import requests

print("""

CATSCOBOT-SOURCE

""")
while True:
  try:
    code = requests.get("https://raw.githubusercontent.com/ethandacat/catscobott/refs/heads/main/prod.py").text
    print("Version Number: "+"".join(code.split("#")).split("\n")[0])
    exec(code)
  except:
    print("""

An error occured.

Developed by ethan.
    """)
