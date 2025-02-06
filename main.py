import subprocess

print("""

CATSCOBOT-SOURCE

""")

while True:
  try:
    print("Version Number: "+open("prod.py","r").read().split("\n")[0])
    subprocess.run("python prod.py", shell=True)
  except:
    print("""

An error occured.

Developed by ethan.
    """)
