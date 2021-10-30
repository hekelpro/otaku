try:
	import requests as req, os, re
	from bs4 import BeautifulSoup as par
except ModuleNotFoundError:
	exit("[×] Module not installed..")

col = lambda code: "\x1b[1;"+str(code)+"m" #> color
logo = """
%s	  ___   ______   ____  __  _  __ __
	 /   \ |      T /    T|  l/ ]|  T  T
	Y     Y|      |Y  %so%s  ||  ' / |  |  |
	|  %sO%s  |l_j  l_j|     ||    \ |  |  |
	|     |  |  |  |  _  ||     Y|  :  |
	l     !  |  |  |  |  ||  .  |l     |
	 \___/   l__j  l__j__jl__j\_j \__,_j

		   %sOtakuDesu scraper%s
""" % (col(91), col(92), col(91), col(92), col(91), col(94), col(00))
url = "https://otakudesu.vip/"

def convert_bytes(num):
	step_unit = 1024
	for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
		if num < step_unit:
			return "%3.1f %s" % (num, x)
		num /= step_unit

def search(query, num=0, DumpLink=[]):
	cek = par(req.get(url+"?s={}&post_type=anime".format(query.replace(" ","+"))).text, "html.parser")
	print("")
	for li in cek.find_all("li", {"style": "list-style:none;"}):
		num += 1
		links = li.find("h2").find("a")
		DumpLink.append(links.get("href"))
		status = re.search("\<b>Status<\/b>\s:\s(\w+)<\/div>", str(li)).group(1)

		print("("+col(93)+str(num)+col(00)+") Judul: "+links.text)
		setGenre = li.find("div", {"class": "set"})
		print(" "*int(len(list(str(num))) + 2)+" Genre: "+", ".join([genre.text for genre in setGenre.find_all("a")]))
		print(" "*int(len(list(str(num))) + 2)+" Status: "+status)
		print("#"*45)
	if len(DumpLink) == 0:
		return False
	else:
		return DumpLink

def chek_support_dl(visit, resoVideo: int):
		url_download = []
		teks = []
		ses = req.Session()
		print(col(92)+"#"*45+col(00))
		cok = par(req.get(visit).text, "html.parser")
		donlod = cok.find("div", {"class": "download"}).findAll("ul")[0]
		donlod = donlod.findAll("li")
		del donlod[0]
		donlod = donlod[resoVideo]
		title = cok.find("h1", {"class": "posttl"}).text
		for dl in donlod.find_all("a"):
			url_download.append(dl.get("href"))
			teks.append(dl.text)
		print("[•] Judul: "+title)
		print("[•] Cek url yang mendukung zippyshare")
		if "zippyshare.com" in str(url_download):
			print("[✓] zippyshare terdeteksi, tunggu sebentar")
			getsUrl = par(ses.get("".join(re.findall("(https?://.*?\.zippyshare.com\/.*?file.html)", str(url_download))), headers={"user-agent": "chrome"}).text, "html.parser")
			files = getsUrl.find("font", {"style": "line-height:22px; font-size: 14px;"}).text
			size = "".join(re.findall("Size:.*?\">(.*?)</font>", str(getsUrl)))
			dld = re.findall("document\.getElementById\('dlbutton'\)\.href\s=\s\"(.*?)\"\s\+\s(\(.*?\))\s\+\s\"(.*?)\";", str(getsUrl))[0]
			dur = re.search("(https?://.*?\.zippyshare.com)", str(url_download)).group(1)
			print("[>] Nama files: "+files)
			print("[>] Size video: "+size)

			#-> execute
			downloader = dur+dld[0]+str(eval(dld[1]))+dld[-1]
			r = ses.get(downloader, headers={"user-agent": "chrome"}, stream=True)
			with open("otaku/"+files, "wb") as sv:
				total_length = int(r.headers.get('content-length'))
				readsofar = 0
				for chunk in r.iter_content(chunk_size=1024):
					if chunk:
						readsofar += len(chunk)
						print("\r[!] Downloading "+str(int(readsofar / total_length * 100))+"% ("+str(convert_bytes(readsofar))+" | "+str(convert_bytes(total_length))+") ", end="")
						sv.write(chunk)
						sv.flush()
				sv.close()
			print("\n[✓] Tersimpan:%s otaku/%s%s" % (col(92), files, col(00)))
			print("[✓] Selesai...")
		else:
			print("[-] ZippyShare tidak terdeteksi, silahkan download manual")
			for judul, dol in zip(teks, url_download):
				print("[>] "+judul+": "+dol)


def eps_chekin(links, mahou=[], rev=[]):
	global url
	os.system("clear")
	print(logo)
	cek = par(req.get(links).text, "html.parser")
	sins = cek.find("div", {"class": "infozingle"})
	for span in sins.find_all("span"):
		print(" "*3+" >> "+span.text)
	print(" "*3+" >> sinopsis: "+cek.find("div", {"class": "sinopc"}).text)
	lii = cek.findAll("ul")[3]
	for eps in lii.find_all("li"):
		rev.append(eps.find("a").get("href"))
	if len(rev) == 0:
		print("\n[×] Tidak ada episode yang bisa di ambil")
		input("[=] Enter untuk kembali "); main_menu()
	else:
		print("\n[•] Episode berjumlah %s%s%s" % (col(92), str(len(rev)), col(00)))
		print("[+] Ex: Masukan episode yang ingin anda unduh, ex: 1")
		print("      : Gunakan koma untuk multi download, ex: 3,5,6")
		print("      : Masukan inputan All untuk download semua episode, ex: all")
		whileEps = input("[?] Mau unduh yang mana: ")
		resolusi = input("[?] Mau video hd/sd? [h/s]: ").lower()
		while resolusi not in ["s","h"]:
			resolusi = input("[?] Mau video hd/sd? [h/s]: ").lower()
		print(""); [mahou.append(_) for _ in reversed(rev)]
		if resolusi == "s":
			res = 0
		else:
			res = -1

		if whileEps.lower().strip() == "all":
			for mausama in mahou:
				try:
					chek_support_dl(mausama, res)
				except:
					print("[!] Gomene senpai :), tools ini hanya bisa download per-episode\n    Langsung saja kunjungi situs {}".format(url))
			print(col(92)+"#"*45+col(00), "\n")
		else:
			for delim in whileEps.split(","):
				try:
					maou = mahou[int(delim)-1]
					chek_support_dl(maou, res)
				except:
					print("[!] Gomene senpai :), tools ini hanya bisa download per-episode\n    Langsung saja kunjungi situs {}".format(url))
			print(col(92)+"#"*45+col(00), "\n")

def main_menu():
	os.system("clear")
	print(logo)
	print(">_< Welcome darling, semoga kamu suka dengan tools ini")
	query = input("[•] Cari anime: ")
	while query == "":
		query = input("[•] Cari anime: ")
	cari = search(query)
	if cari == False:
		exit("[+] Anime yang anda cari tidak ada\n")
	else:
		pilih = input("\n[?] Pilih pencarian: ")
		while int(pilih) > len(cari) or not pilih.isdigit():
			pilih = input("[?] Pilih pencarian: ")
		try:
			chs = cari[int(pilih)-1]
		except Exception as ex:
			exit("[×] ERROR: "+str(ex)+"\n")
		print("[!] Tunggu Sebentar")
		eps_chekin(chs)


if __name__=="__main__":
	try:
		os.mkdir("otaku")
	except:
		pass
	main_menu()
