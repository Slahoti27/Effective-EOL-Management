"""Palo Alto"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")


class PaloAlto_Scraper:
    """Palo Alto Scraper Class"""

    url = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary"

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

        tables = self.driver.find_elements(By.XPATH, "//table")
        list_of_df=[]

        def contructDataFrame(table):
            mainList=[]

            rows = table.find_elements(By.XPATH, './/tr')

            for row in rows[2:]:
                tempList=[]

                data=row.find_elements(By.XPATH, ".//td | .//th")

                for datum in data:
                    tempList.append(datum.text)
                mainList.append(tempList)

            df=pd.DataFrame(mainList[1:], columns=mainList[0])
            return df

        for table in tables:
            temp = contructDataFrame(table)
            list_of_df.append(temp)

        final_df=pd.concat(list_of_df)
        final_df["End-of-Life Date"] = final_df["End-of-Life Date"].apply(lambda x: self.convert_and_fill_date(x))
        # df.drop(df[df['End-of-Life'] == 'See note'].index, inplace=True)
        final_df['Source URL'] = url
        final_df["Vendor"]="Paloalto"
        final_df = final_df[~final_df['End-of-Life Date'].str.contains('*', na=False)]
        final_df.to_csv(output_filename, index=False)
        self.driver.close()
        return final_df


#Calling the function and getting the CSV file
scraper = PaloAlto_Scraper()
scraper.eol_data_generator(scraper.url, "CSV\SW\PaloAlto.csv")