from selenium import webdriver
# browser = webdriver.Firefox() # original goat example code
# note: replace the url with your docker's ip address + your selenium hub's docker port number (can be found via "docker ps")
selenium_hub_url = 'http://192.168.99.100:4444/wd/hub'
# open firefox browser on selenium hub
browser = webdriver.Remote(
 command_executor=selenium_hub_url,
 desired_capabilities={"browserName": "firefox"})
# note: replace the url with your docker's ip address + your django app's port number (can be found in )
django_url = 'http://192.168.99.100:8000'
# go to django app url (assume django app is up)
browser.get(django_url)
assert 'Django' in browser.title