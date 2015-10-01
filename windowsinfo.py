#!/usr/bin/env python
#!/c/Python27/python.exe
import getpass
user = str(getpass.getuser())
client = '''C:\Users\\"%s"\\AppData\\Roaming\\IMVUClient\\imvuclient.exe'''%(user)
def path():
	return client