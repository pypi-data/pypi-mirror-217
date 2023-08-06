from selenium import webdriver
from selenium.webdriver.chrome.service import Service
def Browser(url, show=False):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    if show is False:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, service=Service("chromedriver.exe"))
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      })
    """
    })
    driver.maximize_window()
    driver.get(url)
    return driver