import requests
import codecs
from bs4 import BeautifulSoup

# We prepare all the parametres for our post request
url = "http://annuairesante.ameli.fr/recherche.html"
payload = {
    "type": "ps",
    "ps_profession": "34",
    "ps_profession_label": "Médecin généraliste",
    "ps_localisation": "HERAULT (34)",
    "localisation_category": "departements",
}
header = {
    "Content-type": "text/html", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

# Creating session to get the cookies needed for the request
s = requests.Session()

# We make the request and store the response in page
page = s.post(url, params=payload, headers=header)

# Saving the html structure in html file
f = codecs.open("./text.html", "w", "utf-8")
f.write(page.text)
f.close()

# We parse the html code to get the needed data
soup = BeautifulSoup(page.text, 'html.parser')

# print(soup.prettify())
allDivs = soup.find_all("div", {"class": "item-professionnel-inner"})

for div in allDivs:
    # We prepare an object medecin with all the data we want
    medecin = {"lastName": "", "firstName": "", "adresse": "", "telephone": ""}
    
    # We get all the data required for our object
    medecin["lastName"] = div.find_all("div", {"class": "nom_pictos"})[0].find_all("h2", {"class": "ignore-css"})[0].a.find_all("strong")[0].text
    medecin["firstName"] = div.find_all("div", {"class": "nom_pictos"})[0].find_all("h2", {"class": "ignore-css"})[0].a.text[len(medecin["lastName"])+1:]
    medecin["adresse"] = div.find_all("div", {"class": "adresse"})[0].text

    # All medecin doesn't have a telephone number so we have to take care of those without any
    try:
        tel = (div.find_all("div", {"class": "tel"})[0].text)
        tel = tel.split()
        # Join method doesn't work for some reasons so we use the concatenation of string via "+"
        medecin["telephone"] = tel[0]+tel[1]+tel[2]+tel[3]+tel[4]
    except:
        medecin["telephone"] = "Not any"
        
    # We display our medecin in the terminal
    print("---------")
    print(medecin)



# print(page.request.headers)
print(page.status_code)
# print(page.text)