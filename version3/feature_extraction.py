import ipaddress
import re
import urllib.request
from bs4 import BeautifulSoup
import socket
import requests
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse
from urllib.parse import urlparse
from Levenshtein import distance as levenshtein_distance


# test_url = 'https://iehraz.adliran.ir/Login/Authenticate?ReturnUrl=http://adliran.ir/JssClearanceCertRequest/SelfIndex&SystemName=JssClearanceCertRequestService&isSelectNaturalPerson=True&isSelectNaturalForigenPerson=False&isSelectLegalPerson=False&isSelectJudPerson=False&LoginTitle=%d8%ab%d8%a8%d8%aa%20%d8%af%d8%b1%d8%ae%d9%88%d8%a7%d8%b3%d8%aa%20%da%af%d9%88%d8%a7%d9%87%db%8c%20%d8%b9%d8%af%d9%85%20%d8%b3%d9%88%d8%a1%20%d9%be%db%8c%d8%b4%db%8c%d9%86%d9%87'
# htmlpage = 'C:\\Users\\styxm\\Desktop\\models\\1140159.txt'

# DATASET
def feature_extraction(htmlpage ,url, label):

# # Extraction 
# def feature_extraction(url):

  features = []
  url = url
  domain = ""
  urlparse = ""
  soup = ""

  # ONLINE
  # try:
  #     response = requests.get(url)
  #     soup = BeautifulSoup(response.text, 'html.parser')
  # except:
  #     pass
  
  try:
    with open(htmlpage, 'r', encoding='utf8') as html_file:
      content = html_file.read()

      soup = BeautifulSoup(content, 'lxml')

  except:
      pass



  try:
      urlparse = urlparse(url)
      domain = urlparse.netloc
  except:
      pass



  def UsingIp():
      try:
          ipaddress.ip_address(url)
          return -1
      except:
          return 1

  def longUrl():
      return len(url)



  def shortUrl():
      match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                  'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                  'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                  'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                  'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                  'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                  'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
      if match:
          return -1
      return 1


  
  def redirecting():
      if url.rfind('//')>6:
          return -1
      return 1

  def SubDomains():
      dot_count = len(re.findall("\.", url))
      return dot_count

  # 8.HTTPS
  def Hppts():
      try:
          https = urlparse.scheme
          if 'https' in https:
              return 1
          return -1
      except:
          return 1


  def Favicon():
      try:
          for head in soup.find_all('head'):
              for head.link in soup.find_all('link', href=True):
                  dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                  if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                      return 1
          return -1
      except:
            return -1

  def NonStdPort():
      try:
          port = domain.split(":")
          return len(port)
      except:
          return -1

    
  def SRC_Check():
      i, success, LD = 0, 0, 0
      try:

          for img in soup.find_all('img', src=True):
              dots = [x.start(0) for x in re.finditer('\.', img['src'])]
              if url in img['src'] or domain in img['src'] or len(dots) == 1:
                  success = success + 1
                  LD += levenshtein_distance(url, img['src'])/ max([len(url), len(img['srce'])])
              i = i+1

          for audio in soup.find_all('audio', src=True):
              dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
              if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                  success = success + 1
                  LD += levenshtein_distance(url, audio['src'])/ max([len(url), len(audio['src'])])
              i = i+1

          for embed in soup.find_all('embed', src=True):
              dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
              if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                  success = success + 1
                  LD += levenshtein_distance(url, embed['src'])/ max([len(url), len(embed['src'])])
              i = i+1

          for iframe in soup.find_all('iframe', src=True):
              dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
              if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                  success = success + 1
                  LD += levenshtein_distance(url, iframe['src'])/ max([len(url), len(iframe['src'])])
              i = i+1

          for script in soup.find_all('script', src=True):
              dots = [x.start(0) for x in re.finditer('\.', script['src'])]
              if url in script['src'] or domain in script['src'] or len(dots) == 1:
                  success = success + 1
                  LD += levenshtein_distance(url, script['src'])/ max([len(url), len(script['src'])])

              i = i+1

          try:
              percentage = success/float(i)
              LD_result = LD / i
              return round(percentage, 3), round(LD_result, 3)
          except:
              return 0
      except:
          return -1
    
  def AnchorURL():
      try:
          i,unsafe = 0,0
          for a in soup.find_all('a', href=True):
              if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                  unsafe = unsafe + 1
              i = i + 1

          try:
              percentage = unsafe / float(i)
              return round(percentage, 3)
          except:
              return -1

      except:
            return -1

  def HREF_Check():
      try:
          i,success, LD = 0, 0, 0
      
          for link in soup.find_all('link', href=True):
              dots = [x.start(0) for x in re.finditer('\.', link['href'])]
              if url in link['href'] or domain in link['href'] or len(dots) == 1:
                  success = success + 1
                  LD += levenshtein_distance(url, link['href'])/ max([len(url), len(link['href'])])

              i = i+1



          for a in soup.find_all('a', href=True):
              dots = [x.start(0) for x in re.finditer('\.', a['href'])]
              if url in a['href'] or domain in a['href'] or len(dots) == 1:
                  success = success + 1
                  LD += levenshtein_distance(url, a['href'])/ max([len(url), len(a['href'])])
              i = i+1


          try:
              percentage = success / float(i)
              LD_result = LD / i
              return round(percentage, 3), round(LD_result, 3)
          except:
              return 0
      except:
          return -1

  def ServerFormHandler():
      try:
          if len(soup.find_all('form', action=True))==0:
              return 1
          else :
              for form in soup.find_all('form', action=True):
                  if form['action'] == "" or form['action'] == "about:blank":
                      return -1
                  elif url not in form['action'] and domain not in form['action']:
                      return 0
                  else:
                      return 1
      except:
          return -1

  def InfoEmail():
      try:
          if re.findall(r"[mail\(\)|mailto:?]", soup):
              return -1
          else:
              return 1
      except:
          return -1


  def StatsReport():
      try:
          url_match = re.search(
      'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
          ip_address = socket.gethostbyname(domain)
          ip_match = re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                              '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                              '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                              '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                              '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                              '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
          if url_match:
              return -1
          elif ip_match:
              return -1
          return 1
      except:
          return 1

  # 4.Symbol@
  def symbol():
      if re.findall("@",url):
          return -1
      return 1

  
  # 6.prefixSuffix
  def prefixSuffix():
      try:
          match = re.findall('\-', domain)
          if match:
              return -1
          return 1
      except:
            return -1


  features.append(UsingIp())
  features.append(longUrl())
  features.append(shortUrl())
  features.append(symbol())
  features.append(redirecting())
  features.append(prefixSuffix())
  features.append(SubDomains())
  features.append(Hppts())
  features.append(Favicon())
  features.append(NonStdPort())
  try:
    features += SRC_Check()  
  except:
    features.append(SRC_Check())
  features.append(AnchorURL())
  try:
    features += HREF_Check()  
  except:
    features.append(HREF_Check())
  features.append(ServerFormHandler())
  features.append(InfoEmail())
  features.append(StatsReport())

  return features


# print(feature_extraction(htmlpage, test_url, 1))

