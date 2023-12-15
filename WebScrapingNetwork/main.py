from seleniumwire import webdriver
import pandas as pd
import dns.resolver
import re
import easygui

def get_webpage_data(url):
    """
    This function takes a URL as input, visits the webpage using Selenium,
    and returns a dictionary mapping websites to their IP addresses.
    """

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
            website = re.search('https?://([^/]*)/', request.url).group(1)
            ip = dns.resolver.resolve(website, 'A')
            ips = '\n'.join(ipval.to_text() for ipval in ip)
            data[website] = ips

    return data

def save_data_to_excel(data, filename):
    """
    This function takes a dictionary and a filename as input,
    and writes the data to an Excel file.
    """

    # Convert dictionary to a pandas DataFrame
    web_ip = pd.DataFrame(list(data.items()), columns=['Website', 'IP'])
    web_ip['IP'] = web_ip['IP'].astype(str)

    # Write the weburl&ip to an Excel file
    web_ip.to_excel(filename, index=False)

if __name__ == "__main__":
    # Show an input box for the user to enter the URL
    url = easygui.enterbox(msg='Enter the URL:', title='URL Input')

    data = get_webpage_data(url)

    save_data_to_excel(data, 'websiteip.xlsx')
