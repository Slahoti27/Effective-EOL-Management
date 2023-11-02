"""Barracuda Campus"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")


class Barracuda_Campus_Scraper:
    """Barracuda Campus Scraper Class"""

    url = "https://campus.barracuda.com/product/cloudgenfirewall/doc/71860841/barracuda-nextgen-and-cloudgen-firewall-appliances-eos-eol-definitions/"

    def __init__(self):
        self.driver = None
    
    def open_url(self, url):
        """Common Function for opening the URL in Chrome"""
        self.driver = webdriver.Chrome("Program Files\chromedriver.exe")
        self.driver.get(url)
        time.sleep(10)
    
    def eol_data_generator(self, url, output_filename):
        """scrape_data function collects the data
        : returns dataframe and CSV file"""
        self.open_url(url)

        table = self.driver.find_element(By.XPATH, "//table")
        print(table.text)
        mainList=[]
        rows=table.find_elements(By.XPATH, './/tr')
        for row in rows:
            tempList=[]
            data=row.find_elements(By.XPATH, ".//td | .//th")
            for datum in data:

                tempList.append(datum.text)

            mainList.append(tempList)

        df = pd.DataFrame(mainList[1:], columns=mainList[0])

        df['Source URL'] = url
        df['Vendor'] = 'Barracuda Campus'

        #Converted dataframe to CSV
        df.to_csv(output_filename, index=False)
        print(df)
        self.driver.close()
        return df


#Calling the function and getting the CSV file
scraper = Barracuda_Campus_Scraper()
scraper.eol_data_generator(scraper.url, "CSV\HW\Barracuda.csv")