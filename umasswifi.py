import requests
from .secret import username, password
aruba_url = 'https://securelogin.arubanetworks.com/upload/custom/cp-UMASS/login.html?cmd=login'
post_url_postfix = '/cgi-bin/login'
test_url = 'http://kang.wogloms.com/ok.html'

try:
	initial = requests.get("http://1.1.1.1", timeout=1, verify=False)
except requests.exceptions.ConnectTimeout:
	print("You appear to be already connected.")
	exit(0)

if initial.status_code == 200:
	redir_url = initial.text.split("url=")[1].split("'>")[0]
	redir = requests.get(redir_url, verify=False)

	if redir.status_code == 200:
		if "login.wireless.umass.edu" in redir.url:
			post_url = "https://login.wireless.umass.edu" + post_url_postfix
		elif "securelogin.arubanetworks.com" in redir.url:
			post_url = "https://securelogin.arubanetworks.com" + post_url_postfix
		else:
			print("URL: ", redir.url)
			exit(0)
		print("Login URL:", post_url)
		login = requests.post(post_url, data={
			'user': username,
			'password': password,
			'login_submit': 'Log in'
		}, verify=False)

		print(login.status_code)
		if "errmsg=" in login.url:
			print("Failed!")
			exit(0)
		print(login.url)

		test = requests.get(test_url)
		if test.status_code == 200 and test.text.strip() == 'ok':
			print("Connected!")
		else:
			print(test.text)
			print("Not connected. Response:", test.status_code)