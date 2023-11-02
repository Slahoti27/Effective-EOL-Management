"""Cisco Meraki"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")


class Cisco_Meraki_Scraper:
    """Cisco_Meraki Scraper Class"""

    url = "https://documentation.meraki.com/General_Administration/Other_Topics/Meraki_End-of-Life_(EOL)_Products_and_Dates"

    def __init__(self):
        self.driver = None
    
    def open_url(self, url):
        """Common Function for opening the URL in Chrome"""
        self.driver = webdriver.Chrome("Program Files\chromedriver.exe")
        self.driver.get(url)
        time.sleep(10)
   
    def convert_and_fill_date(self, date_string):
        try:
            date = pd.to_datetime(date_string, errors='raise')
            
            # Check if the date contains only year and month (day is missing)
            if date.day == 1:
                # If yes, calculate the last day of the month
                date += pd.offsets.MonthEnd(0)

            # Convert the datetime to the desired format "YYYY-MM-DD"
            formatted_date = date.strftime("%Y-%m-%d")
            return formatted_date
        except:
            return date_string
    
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

        columns_to_process = ["Announcement", "End-of-Sale Date", "End-of-Support Date"]

        for column in columns_to_process:
            df[column] = df[column].apply(lambda x: self.convert_and_fill_date(x))

        df['Source URL'] = url
        df['Vendor'] = 'Cisco Meraki'

        #Converted dataframe to CSV
        df.to_csv(output_filename, index=False)
        print(df)
        self.driver.close()
        return df


#Calling the function and getting the CSV file
scraper = Cisco_Meraki_Scraper()
scraper.eol_data_generator(scraper.url, "CSV\Hybrid\Cisco_Meraki.csv")