from selenium import webdriver

class Navigator():
    CHROME_DRIVERPATH = './chromedriver'
    CREDENTIALS_PATH = 'credentials.txt'

    def __init__(self, start_page = 'https://ilias.uni-marburg.de/login.php?target=&client_id=UNIMR&auth_stat='):
        download_dir = "./downloads/"
        options = webdriver.ChromeOptions()

        profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
                   # Disable Chrome's PDF Viewer
                   "download.default_directory": download_dir, "download.extensions_to_open": "applications/pdf"}
        options.add_experimental_option("prefs", profile)
        self.driver = webdriver.Chrome(self.CHROME_DRIVERPATH, chrome_options=options)
        self.driver.get(start_page)

    def sign_in(self):
        with open(self.CREDENTIALS_PATH) as file:
            username, password = file.readlines()
            username = username.replace('\n', '')
        username_id = 'username'
        username_webelement = self.driver.find_element_by_id(username_id)
        username_webelement.send_keys(username)
        password_id = 'password'
        password_webelement = self.driver.find_element_by_id(password_id)
        password_webelement.send_keys(password)
        anmelden_name = 'cmd[doStandardAuthentication]'
        anmelden_webelement = self.driver.find_element_by_name(anmelden_name)
        anmelden_webelement.click()