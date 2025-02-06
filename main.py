import subprocess
import requests

print("""

CATSCOBOT-SOURCE

""")

while True:
  try:
    print("Version Number: "+open("prod.py","r").read().split("\n")[0])
    exec(requests.get("").text)
  except:
    print("""

An error occured.

Developed by ethan.
    """)
