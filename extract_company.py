import requests
from urllib.parse import urlparse


def get_company_if_valid(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        input_parsed = urlparse(url)
        input_domain = input_parsed.hostname.replace("www.", "").split('.')[0] # "arsh"
    except:
        return "Invalid URL format"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        
        if response.status_code >= 400:
            return None

        final_url = response.url
        final_parsed = urlparse(final_url)
        final_domain = final_parsed.hostname.replace("www.", "") 

        
        known_sellers = ["hugedomains", "godaddy", "namecheap", "dan.com", "sedo", "afternic"]

        for seller in known_sellers:
            if seller in final_domain:
                return None 

        content = response.text.lower()
        start_title = content.find('<title>')
        end_title = content.find('</title>')
        
        if start_title != -1 and end_title != -1:
            page_title = content[start_title:end_title]
            
            bad_titles = ["domain is for sale", "domain available", "parked", "buy this domain"]
            for bad in bad_titles:
                if bad in page_title:
                    return None

        return input_domain

    except Exception as e:
        return None
