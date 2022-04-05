from flask import Flask, render_template, request
import urllib.request, re, datetime, time

app = Flask(__name__)

klima = False
osu = False
nawil = False
ogrz = False

@app.route('/')
def index():
	
	start = datetime.datetime.now().second
	godziny = datetime.datetime.now().hour -1
	minuty = datetime.datetime.now().minute -1


	#print(htmlSource)

	#x = re.search("temperature", str(htmlSource))
	#print(x)


	#print("minuta:" + str(minuty))  
	godziny = datetime.datetime.now().hour -1
	minuty = datetime.datetime.now().minute -1
	sekundy = datetime.datetime.now().second
	if (godziny < 10 and minuty < 10):
		sock = urllib.request.urlopen("https://unasdziala.blob.core.windows.net/cos/94dd2151-1cc6-4de3-95fd-e9276ac970a0/12/2022/03/26/0"+str(godziny)+"/0"+str(minuty)+"/q3npkur4s4eqe")
	if (godziny < 10 and minuty >= 10):
		sock = urllib.request.urlopen("https://unasdziala.blob.core.windows.net/cos/94dd2151-1cc6-4de3-95fd-e9276ac970a0/12/2022/03/26/0"+str(godziny)+"/"+str(minuty)+"/q3npkur4s4eqe")
	if (godziny >= 10 and minuty < 10):
		sock = urllib.request.urlopen("https://unasdziala.blob.core.windows.net/cos/94dd2151-1cc6-4de3-95fd-e9276ac970a0/12/2022/03/26/"+str(godziny)+"/0"+str(minuty)+"/q3npkur4s4eqe")
	if (godziny >= 10 and minuty >= 10):
		sock = urllib.request.urlopen("https://unasdziala.blob.core.windows.net/cos/94dd2151-1cc6-4de3-95fd-e9276ac970a0/12/2022/03/26/"+str(godziny)+"/"+str(minuty)+"/q3npkur4s4eqe")
	htmlSource = sock.read()                            
	sock.close() 
	temperatury = re.findall("\"temperature\":\d+.\d+", str(htmlSource))
	wilgotnosci = re.findall("\"humidity\":\d+.\d+", str(htmlSource))
	cisnienia = re.findall("\"pressure\":\d+.\d+", str(htmlSource))
	natezenia = re.findall("\"light\":\d+.\d+", str(htmlSource))
	#time.sleep(5)
	#print(temperatury[-1])	
	#return temperatury[-1]
	temperaturka = (temperatury[-1].split(":"))
	wilgotnoscik = (wilgotnosci[-1].split(":"))
	cisnionko = (cisnienia[-1].split(":"))
	print("natezenia", natezenia)
	natezonko = (natezenia[-1].split(":"))

	if float(temperaturka[1])< 10:
		temp = "Wyłączam klimatyzację!"
		klima = False
		ogrz = True
		time.sleep(10)
		temp = "Klimatyzacja wyłaczona"
	elif float(temperaturka[1]) > 28:
		temp = "Wyłączam ogrzewanie!"
		klima = True
		ogrzewanie = False
		time.sleep(10)
		temp = "Klimatyzacja włączona"
	else:
		temp = "Jest prawidłowa!"
		klima = False
		ogrz = False
	
	if float(wilgotnoscik[1])< 40:
		wilg = "Włączam nawilżacz powietrza!"
		nawil = True
		osu = False
		time.sleep(10)
		wilg = "Nawilżacz powietrza włączony"
	elif float(wilgotnoscik[1]) > 45:
		wilg = "Osuszacz powietrza włączony"
		nawil = False
		osu = True
		time.sleep(10)
		
	else:
		wilg = "Jest prawidłowa!"
		nawil = False
		osu = False

	
	if float(cisnionko[1])< 90 or float(cisnionko[1]) > 110:
		cis = "Jest nieprawidłowe!"
	else:
		cis = "Jest prawidłowe!"
	
	if float(natezonko[1]) < 300:
		nat = "Podnoszę rolety!"

	elif float(natezonko[1]) > 700:
		nat = "Opuszam rolety!"
	else:
		nat = "Jest prawidłowe!"
	
	
	godzinki = godziny + 1
	minutki = minuty + 1

	if godzinki < 10:
		godzinki = "0" + str(godzinki)
	if minutki < 10:
		minutki = "0" + str(minutki)
	
	
	return render_template('index.html', wilgotnoscopis= wilg, temperaturaopis= temp, cisnienieopis= cis, natezenieopis= nat, godzina = godzinki, minuty = minutki, temperatura=temperaturka[1], wilgotnosc = wilgotnoscik[1], cisnienie = cisnionko[1], natezenie = natezonko[1])




if __name__ == "__main__":
	app.run(debug = True)

