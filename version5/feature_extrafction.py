import ipaddress
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# test_url = 'https://www.iehraz.adliran.ir/Login/Authenticate?ReturnUrl=http://adliran.ir/JssClearanceCertRequest/SelfIndex&SystemName=JssClearanceCertRequestService&isSelectNaturalPerson=True&isSelectNaturalForigenPerson=False&isSelectLegalPerson=False&isSelectJudPerson=False&LoginTitle=%d8%ab%d8%a8%d8%aa%20%d8%af%d8%b1%d8%ae%d9%88%d8%a7%d8%b3%d8%aa%20%da%af%d9%88%d8%a7%d9%87%db%8c%20%d8%b9%d8%af%d9%85%20%d8%b3%d9%88%d8%a1%20%d9%be%db%8c%d8%b4%db%8c%d9%86%d9%87'
# htmlpage = 'C:\\Users\\styxm\\Desktop\\models\\1140159.txt'

def feature_extraction(htmlpage, url, label):

    with open(htmlpage, 'r', encoding='utf8') as html_file:
        content = html_file.read()

        soup = BeautifulSoup(content, 'lxml')

    parse = urlparse(url)
    domain = parse.netloc
    subdomains = parse.netloc.split('.')[:-2]
    tld = parse.netloc.split('.')[-1]
    path = parse.path
    query = parse.query


    # copyright
    text = ''
    try:
        for text in soup.stripped_strings:
            if '©' in text:
                text = re.sub(r'\s+', ' ', text)  
    except:
        pass


    # FEATURES #


    # subdomain level
    f1 = len(subdomains) 


    # com in subdomains
    f2 = 1
    f5 = 0
    f9 = 0
    f19 = 1
    for i in subdomains:
        if re.findall(i, text):
            f19 = -1
        f5 += len(i)
        for a in i:
            if a.isdigit():
                f9 += 1
        if re.findall('com', i):
            f2 = -1


    # UsingIp
    f3 = 1
    try:
        ipaddress.ip_address(url)
        f3 = -1
    except:
        pass


    # Common Top-level Domain 
    f4 = -1
    tlds = ['com', 'org', 'net', 'edu', 'gob', 'int', 'gov', 'mil', 'ir', 'co']
    if tld in tlds:
        f4 = 1

    # U5.1, U5.2 , U5.3, U5_4
    # Length: count the characters within the subdomain U5.1, the domain U5.2, the path U5.3, query
    f6, f7, f8 = 0, 0, 0
    f6 = len(parse.netloc.split('.')[-2])
    f7 = len(path)
    f8 = len(query)

    # U6.1, U6.2, U6.3
    # Digits: count the number of digits in the subdomain U6.1, the domain U6.2 and the path U6.3   
    f10, f11, f12 = 0, 0, 0
    for i in parse.netloc.split('.')[-2]:
        if i.isdigit():
            f10 += 1
    for i in path:
        if i.isdigit():
            f11 += 1
    for i in query:
        if i.isdigit():
            f12 += 1

   # Special characters '@' (U7.1) ,‘.’ (U7.2), ‘/’ (U7.3), ‘@’ (U7.4), ‘?’ (U7.5), ‘=’ (U7.6), ‘_’ (U7.7), ‘&’ (U7.8) and ‘˜’ (U7.9). 
    # These features are set to the times each symbol appeared on the entire URL. 
    f13 = 0
    specialCharList = ['-', '@', '?', '=', '_', '&', '~']
    domain_path = parse.netloc + parse.path
    for i in domain_path:
        if i in specialCharList:
            f13 += 1


    # external , internal , samepage  (#), empty , null 
    external, internal, samepage, empty, null,i = 0, 0, 0, 0, 0, 0

    try:
        for img in soup.find_all('img', src=True):
            dots = [x.start(0) for x in re.finditer('\.', img['src'])]
            if img['src'] == '#':
                samepage += 1
            elif url in img['src'] or domain in img['src'] or len(dots) == 1:
                internal += 1
            elif "#" in img['src'] or "javascript" in img['src'] .lower() or "mailto" in img['src'] .lower() or not (url in img['src']  or domain in img['src'] ) or img['src'] == '' or img['src'] == None:
                    empty += 1
            else:
                external += 1
            i = i+1

        for script in soup.find_all('script', src=True):
            dots = [x.start(0) for x in re.finditer('\.', script['src'])]
            if script['src'] == '#':
                samepage += 1
            elif url in script['src'] or domain in script['src'] or len(dots) == 1:
                internal += 1
            elif "#" in script['src'] or "javascript" in script['src'] .lower() or "mailto" in script['src'] .lower() or not (url in script['src']  or domain in script['src'] ) or script['src'] == '' or script['src'] == None:
                    empty += 1
            else:
                external += 1
            i = i+1


        for link in soup.find_all('link', src=True):
            dots = [x.start(0) for x in re.finditer('\.', link['href'])]
            if link['href'] == '#':
                samepage += 1
            elif url in link['href'] or domain in link['href'] or len(dots) == 1:
                internal += 1
            elif "#" in link['href'] or "javascript" in link['href'] .lower() or "mailto" in link['href'].lower() or not (url in link['href']  or domain in link['href'] ) or link['href'] == '' or link['href'] == None:
                    empty += 1
            else:
                external += 1
            i = i+1


        for a in soup.find_all('a', src=True):
            dots = [x.start(0) for x in re.finditer('\.', a['href'])]
            if a['href'] == '#':
                samepage += 1
            elif url in a['href'] or domain in a['href'] or len(dots) == 1:
                internal += 1
            elif "#" in a['href'] or "javascript" in a['href'] .lower() or "mailto" in a['href'].lower() or not (url in a['href']  or domain in a['href'] ) or a['href'] == '' or a['href'] == None:
                    empty += 1
            else:
                external += 1
            i = i+1

    except:
        pass



    try:
        null += len(soup.find_all('img', src=False))
        null += len(soup.find_all('script', src=False))
        null += len(soup.find_all('a', href=False))
        null += len(soup.find_all('link', href=False))
        i += null

    except:
        pass


    f14 = len(soup.text)

    # shortURL
    f15 = 1
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                  'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                  'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                  'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                  'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                  'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                  'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
    if match:
          f15 = -1


    # copyright exists
    f16 = -1
    if text != '':
        f16 = 1

    # domain in html
    f17 = -1
    if re.findall(domain, soup.text) or re.findall(parse.netloc.split('.')[-2], soup.text):
        f17 = 1

    # domain in copyright
    f18 = -1
    if re.findall(domain, text) or re.findall(parse.netloc.split('.')[-2], text):
        f18 = 1

    # redirect
    f19 = 1
    if url.rfind('//')>6:
          f19 = -1


    # SSL
    f20 = -1
    try:
          https = urlparse.scheme
          if 'https' in https:
              f20 = 1
          f20 = -1
    except:
          f20 = 1


    # favicon
    f21 = -1
    try:
          for head in soup.find_all('head'):
              for head.link in soup.find_all('link', href=True):
                  dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                  if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                      f21 = 1
          f21 = -1
    except:
            f21 = -1

    
    # form handler
    f22 = -1
    try:
          if len(soup.find_all('form', action=True))==0:
              f22 = 1
          else :
              for form in soup.find_all('form', action=True):
                  if form['action'] == "" or form['action'] == "about:blank":
                      f22 = -1
                  elif url not in form['action'] and domain not in form['action']:
                      f22 = 0
                  else:
                      f22 = 1
    except:
        f22 = -1



    # 11. NonStdPort
    f23 = -1
    try:
        port = domain.split(":")
        if len(port)>1:
            f23 = -1
        f23 = 1
    except:
        f23 = -1


    # RequestURL
    f24 = -1 
    f25 = 0
    try:
        for img in soup.find_all('img', src=True):
            dots = [x.start(0) for x in re.finditer('\.', img['src'])]
            if url in img['src'] or domain in img['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for audio in soup.find_all('audio', src=True):
            dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
            if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for embed in soup.find_all('embed', src=True):
            dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
            if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for iframe in soup.find_all('iframe', src=True):
            dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
            if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        try:
            percentage = success/float(i) * 100
            f25 = percentage / 100
            if percentage < 22.0:
                f24 = 1
            elif((percentage >= 22.0) and (percentage < 61.0)):
                f24 = 0
            else:
                f24 = -1
        except:
            f24 = 0
    except:
        f24 = -1



    # 14. AnchorURL
    f26 = -1
    f27 = 0
    try:
        i,unsafe = 0,0
        for a in soup.find_all('a', href=True):
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1

        try:
            percentage = unsafe / float(i) * 100
            f27 = percentage / 100
            if percentage < 31.0:
                f26 = 1
            elif ((percentage >= 31.0) and (percentage < 67.0)):
                f26 = 0
            else:
                f26 = -1
        except:
            f26 = -1

    except:
        f26 = -1



    # 15. LinksInScriptTags
    f28 = -1
    f29 = 0
    try:
        i,success = 0,0
    
        for link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', link['href'])]
            if url in link['href'] or domain in link['href'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for script in soup.find_all('script', src=True):
            dots = [x.start(0) for x in re.finditer('\.', script['src'])]
            if url in script['src'] or domain in script['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        try:
            percentage = success / float(i) * 100
            f29 = percentage / 100
            if percentage < 17.0:
                f28 = 1
            elif((percentage >= 17.0) and (percentage < 81.0)):
                f28 = 0
            else:
                f28 = -1
        except:
            f28 = 0
    except:
        f28 = -1


    url_lenth = len(url)

    try:
        return f1, f2, f3, f4, f5/ url_lenth, f6/ url_lenth, f7/ url_lenth, f8/ url_lenth, f9/ url_lenth, f10/ url_lenth, f11/ url_lenth, f12/ url_lenth, f13/ url_lenth, external/i, internal/i, samepage/i, empty/i, null/i, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, label
    except:
        return f1, f2, f3, f4, f5/ url_lenth, f6/ url_lenth, f7/ url_lenth, f8/ url_lenth, f9/ url_lenth, f10/ url_lenth, f11/ url_lenth, f12/ url_lenth, f13/ url_lenth, 0, 0, 0, 0, 0, f14, f15, f16, f17, f18, f19 , f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, label


# print(feature_extraction(htmlpage, test_url, 1))



