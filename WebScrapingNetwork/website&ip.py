from seleniumwire import webdriver  # Import from seleniumwire
import pandas as pd
import dns.resolver
import re


# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Go to the webpage
driver.get('https://www.163.com')

data = {}

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        pattern = re.compile('https?://([^/]*)/')
        website = pattern.search(request.url)
        ip = dns.resolver.resolve(website.group(1), 'A')
        ips = str()
        for ipval in ip:
            ips+=(ipval.to_text() + '\n')
        data[website.group(1)]=ips

# convert dictionary to a pandas DataFrame
web_ip = pd.DataFrame(list(data.items()), columns=['Website', 'IP'])
web_ip['IP'] = web_ip['IP'].astype(str)
# write the weburl&ip to an Excel file
web_ip.to_excel('website&ip.xlsx', index=False)
        