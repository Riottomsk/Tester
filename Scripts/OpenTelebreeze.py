from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://www.telebreeze.ru")
assert "Telebreeze" in driver.title
driver.close()