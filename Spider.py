import requests
from bs4 import BeautifulSoup as bs
import re
import sys
from termcolor import colored


def banner():
	print("""

░██╗░░░░░░░██╗███████╗██████╗░  ░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗██╗░░░░░███████╗██████╗░
░██║░░██╗░░██║██╔════╝██╔══██╗  ██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██║░░░░░██╔════╝██╔══██╗
░╚██╗████╗██╔╝█████╗░░██████╦╝  ██║░░╚═╝██████╔╝███████║░╚██╗████╗██╔╝██║░░░░░█████╗░░██████╔╝
░░████╔═████║░██╔══╝░░██╔══██╗  ██║░░██╗██╔══██╗██╔══██║░░████╔═████║░██║░░░░░██╔══╝░░██╔══██╗
░░╚██╔╝░╚██╔╝░███████╗██████╦╝  ╚█████╔╝██║░░██║██║░░██║░░╚██╔╝░╚██╔╝░███████╗███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░  ░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝╚═╝░░╚═╝

		""")



def usage():
	print("""

		--single-domain                  only crawl one domain, crawl all domains
		--output                 -o      outout file's name
		--time-out               -t      set a time out for the requests
		--contents			 to save contents of every page
		--urls				 to save only urls

		""")



banner()


args = sys.argv
args.remove(sys.argv[0])


if len(args) < 1 :
	usage()
	exit()

SingleDomain = 0


urls = []
domains = []

OutputFileName = "output.txt"
timeoutValue = ""

n = 0
to_save = "urls"

for arg in args:
	n = n + 1
	if arg.startswith('-'):
		if arg == "-o" or arg == "--output":
			OutputFileName = args[n]
		elif arg == "--single-domain":
			SingleDomain = 1
		elif arg == "--urls":
			to_save = "urls"
		elif arg == "--contents":
			to_save = "contents"
		elif arg == "--timeout" or arg == "-t":
			try :
				timeoutValue = int(args[n])
			except:
				print(colored("[!] ERROR: Please select a valid number for timeout value", 'red'))
				exit()

	else:
		if OutputFileName:
			if arg == OutputFileName:
				pass
		if timeoutValue:
			if arg == timeoutValue:
				pass
		else:
			urls.append(arg)


if len(urls) > 1:
	print(colored("[!] ERROR: more than one url was given", 'red'))
	exit()
elif len(urls) < 1:
	print(colored("[!] ERROR: Please specify a URL", 'red'))
	exit()
else:
	mainURL = urls[0]


with open(OutputFileName, 'w') as f :
	pass





tmpRes = re.findall(r"(.+):\/\/(.+)", mainURL)

proto = tmpRes[0][0]
domain = tmpRes[0][1]





index = 0

string = ""


while urls != []:

	for url in urls:
		index = index + 1
		print(colored(f"[*] Sending request to {url}", 'yellow'))
		try:
			if timeoutValue :
				res1 = requests.get(url = url, timeout = timeoutValue)
			else :
				res1 = requests.get(url)

			if res1.status_code == 200:
				print(colored(f"[+] {url}: {res1.status_code}", 'green'))
			else:
				print(colored(f"[-] {url}: {res1.status_code}", 'red'))
			print(colored(f"[*] Looking for Urls in {url}", 'yellow'))
			soup = bs(res1.text, "html.parser")
			tags = soup.select("a[href]")
			print(colored(f"[+] {len(list(set(tags)))} urls was found in '{url}'", 'green'))
			print(colored("--------------------------------------", 'blue'))
			if SingleDomain == 1 :
				for a in tags:
					alink = a.attrs.get("href")
					if alink.startswith("/"):
						urls.append(proto + "://" + domain + alink)
					elif alink.startswith(url) or re.findall(rf".+:\/\/.*{domain}", url) :
						urls.append(alink)
			elif SingleDomain == 0:
				for a in tags:
					alink = a.attrs.get("href")
					if alink.startswith("/"):
						urls.append(proto + "://" + domain + alink)
					elif alink.startswith(url) or re.findall(rf".+:\/\/.*{domain}", url) :
						urls.append(alink)
					else:
						urls.append(alink)

		except requests.Timeout :
			print(colored(f"[-] {url}: Timeout", "red"))
			print(colored(f"--------------------------------------", "blue"))
		except Exception as err:
			print(colored("[!] ERROR: " + str(err)))
		urls = list(set(urls))
		urls.remove(url)
		if to_save == "urls":
			string = string + url + ": " + str(res1.status_code) + "\n"
		if to_save == "contents":
			string = string + str(res1.text) + "\n\n\n---------------------------------------------------------------------------\n\n\n"

		if index >= 20:
			with open(OutputFileName, "a") as f :
				f.write(string)
				string = ""

with open(OutputFileName, "a") as f:
	f.write(string)


