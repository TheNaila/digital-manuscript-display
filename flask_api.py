import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import random as rand
import json, flask

app = flask.Flask(__name__)

description = []

@app.route("/images", methods=["GET"])
def get_images():
  data = json.loads(flask.request.data)
  params = {
    "s": data['query'],              # The search query
    "type": "all",             # Hidden field value
    "museum": data['college'],           # Selected value from the dropdown
    "t": "objects"  
  }

  response = requests.get("https://museums.fivecolleges.edu/info.php", params=params) 
  soup = BeautifulSoup(response.text, "html.parser")

  results_bar = soup.select('p[align="center"] a')

  #initial request 
  process_images_in_page(response)
  #subsequent pages
  for count, a in enumerate(results_bar):
    result_url = "https://museums.fivecolleges.edu/"+ str(a['href'])
    response = requests.get(result_url)
    process_images_in_page(response)

def process_images_in_page(response):
  soup = BeautifulSoup(response.text, "html.parser")
  td_elements = soup.find_all('td', {'align': 'center', 'valign': 'middle', 'width': '20%'})
  for count, value in enumerate(td_elements):
    img_tag = value.find('img')
    img_url = img_tag['src']
    img_response = requests.get("https://museums.fivecolleges.edu/"+ img_url)
    image = Image.open(BytesIO(img_response.content))
    string = "image_" + str(rand.randint(0, len(td_elements * 1000)))
    image.save(string + ".jpg")