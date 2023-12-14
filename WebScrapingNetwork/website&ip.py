from seleniumwire import webdriver
import pandas as pd
import dns.resolver
import re
import easygui

# Show an input box for the user to enter the URL
url = easygui.enterbox(msg='Enter the URL:', title='URL Input')

# Check if https:// or http:// is present in the URL, if not add it
if not re.match('(?:http|ftp|https)://', url):
    url = 'https://{}'.format(url)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Go to the webpage
driver.get(url)

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

# Convert dictionary to a pandas DataFrame
web_ip = pd.DataFrame(list(data.items()), columns=['Website', 'IP'])
web_ip['IP'] = web_ip['IP'].astype(str)

# Write the weburl&ip to an Excel file
web_ip.to_excel('website&ip.xlsx', index=False)
