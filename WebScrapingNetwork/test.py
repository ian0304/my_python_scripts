from seleniumwire import webdriver  # Import from seleniumwire

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Go to the Google home page
driver.get('https://www.163.com')

#create a file to save URL
with open('url.txt', 'w') as f:

# Access requests via the `requests` attribute
    for request in driver.requests:
        if request.response:
            f.writelines(request.url+'\n')
            '''
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )
            '''