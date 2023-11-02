"""Dell"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")


class Dell_Scraper:
    """Dell Scraper Class"""

    url = "https://relutech.com/eol-eosl/dell/?orderby=date-asc"

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

        df["EOSL Date"] = df["EOSL Date"].apply(lambda x: self.convert_and_fill_date(x))
        # df.drop(df[df['End-of-Life'] == 'See note'].index, inplace=True)
        df['Source URL'] = url
        df['Vendor'] = 'Dell'

        #Converted dataframe to CSV
        df.to_csv(output_filename, index=False)
        print(df)
        self.driver.close()
        return df


#Calling the function and getting the CSV file
scraper = Dell_Scraper()
scraper.eol_data_generator(scraper.url, "CSV\HW\Dell.csv")