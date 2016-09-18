import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.google.com")
        self.assertIn("Google", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("Telebreeze")
        assert "No results found." not in driver.page_source
        elem.send_keys(Keys.RETURN)
        WebDriverWait(self, 20).until(needed_link = driver.find_element_by_partial_link_text("telebreeze.ru"))
        needed_link.click()
                         
            
       

    def tearDown(self):
        self.driver.close()
        

if __name__ == "__main__":
    unittest.main()
