# 1 stands for legitimate
# 0 stands for suspicious
# -1 stands for phishing

from bs4 import BeautifulSoup
import urllib
import bs4
import re
from datetime import datetime
from urllib.parse import urlparse
import urllib.request
import requests
from patterns import *
import pandas as pd
from Levenshtein import distance as levenshtein_distance



# f1 IP address
def having_ip_address(url):
    ip_address_pattern = ipv4_pattern + "|" + ipv6_pattern
    match = re.search(ip_address_pattern, url)
    return -1 if match else 1


# f2 SSL security  or Https token
def Https(url):
    if url is None:
        return -1
    if 'https' in url:
        return 1
    else:
        return -1


# f3 number of dots
def having_sub_domain(url):

    if having_ip_address(url) == -1:
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5]))|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',
            url)
        pos = match.end()
        url = url[pos:]
    num_dots = [x.start() for x in re.finditer(r'\.', url)]
    return len(num_dots)


# f4 f5 f6    host_legnth, query length, path length
def lengths(url):
    parser = urlparse(url)
    host_length = len(parser.netloc)
    query_length = len(parser.query)
    path_length = len(parser.path)
    return [host_length, query_length, path_length]




# def HTML_featurs(htmlpage, url):


#   with open(htmlpage, 'r', encoding='utf8') as html_file:
#     content = html_file.read()



def HTML_featurs(url):


  # with open(htmlpage, 'r', encoding='utf8') as html_file:
  #   content = html_file.read()

  #   soup = BeautifulSoup(content, 'lxml')
    source = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(source,'lxml')


    # get  a tags
    a_tags = soup.find_all('a')

    # get  link tags
    link_tags = soup.find_all('link')

    # get  img tags 
    img_tags = soup.find_all('img')

    # get  script tags
    script_tags = soup.find_all('script')


    # get href from a_tags, links
    a_href = []
    for i in a_tags:
      a_href.append(i.get('href'))

    link_href = []
    for i in link_tags:
      link_href.append(i.get('href'))

    # get src from imgs, scripts
    img_src = []
    for i in img_tags:
      img_src.append(i.get('src'))

    script_src = []
    for i in script_tags:
      script_src.append(i.get('src'))


    ld_values = 0
    https_num = 0 
    for i in a_href:
      if Https(i) == 1:
          https_num += 1
      if i == None:
          i = ''
      ld_values += levenshtein_distance(url, i)/ max([len(url), len(i)])

    if len(a_href) == 0:
      f7 = 0
      f11 = 0
    else:
      f7 = ld_values / len(a_href)
      f11 = https_num / len(a_href)

    ld_values = 0
    https_num = 0 
    for i in link_href:
      if Https(i) == 1:
          https_num += 1
      if i == None:
          i = ''
      ld_values += levenshtein_distance(url, i)/ max([len(url), len(i)])


    if len(link_href) == 0:
      f8 = 0
      f12 = 0
    else:
      f8 = ld_values / len(link_href)
      f12 = https_num / len(link_href)


    ld_values = 0
    https_num = 0 
    for i in img_src:
      if Https(i) == 1:
          https_num += 1
      if i == None:
          i = ''
      ld_values += levenshtein_distance(url, i)/ max([len(url), len(i)])


    if len(img_src) == 0:
      f9 = 0
      f13 = 0
    else:
      f9 = ld_values / len(img_src)
      f13 = https_num / len(img_src)



    ld_values = 0
    https_num = 0 
    for i in script_src:
      if Https(i) == 1:
          https_num += 1
      if i == None:
          i = ''
      ld_values += levenshtein_distance(url, i)/ max([len(url), len(i)])


    if len(script_src) == 0:
      f10 = 0
      f14 = 0
    else:
      f10 = ld_values / len(script_src)
      f14 = https_num / len(script_src)


    return [f7, f8, f9, f10, f11, f12, f13, f14]



# # DATA extraction from DATASET
# def featureExtraction(webpage, url, label):
#     features = []
#     features.append(having_ip_address(url))
#     features.append(Https(url))
#     features.append(having_sub_domain(url))
#     length = lengths(url)
#     features += length
#     f_html = HTML_featurs(webpage, url)
#     features += f_html
#     features.append(label)
#     return features



# DATA extraction from URL
def featureExtractionURL(url):
  features = []
  features.append(having_ip_address(url))
  features.append(Https(url))
  features.append(having_sub_domain(url))
  length = lengths(url)
  features += length
  f_html = HTML_featurs(url)
  features += f_html
  return features



url = 'https://365careers.com/business-intelligence-courses'

print(featureExtractionURL(url))
[1, 1, 1, 14, 0, 30, 0.5345100468735428, 0.5878631414490753, 0.7881970235850675, 0.8336858960108261, 1.0, 0.8947368421052632, 0.5151515151515151, 0.42857142857142855]