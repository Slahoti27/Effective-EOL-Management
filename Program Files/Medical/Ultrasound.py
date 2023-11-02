"""Ultrasound Digital Solutions"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

class Ultrasound:
    """Ultrasound Digital Scraper Class"""
    url = "https://www.gehealthcare.com/products/ultrasound/ultrasound-digital-solutions"
    def __init__(self):
        self.driver = None
    
    def open_url(self, url):
        """Common Function for opening the URL in Chrome"""
        self.driver = webdriver.Chrome("Program Files\chromedriver.exe")
        self.driver.get(url)
        self.driver.maximize_window()


    def click_element_by_xpath(self, parent, xpath):
        """Helper function to click an element identified by XPath"""
        element = parent.find_element(By.XPATH, xpath)
        element.click()
        time.sleep(5)

    list_of_dict = []

    def common_dict(self, model_name, product_url, vendor):
        """Helper function to append the data into list of dictionary
        :returns list of dictionary """
        for model, url in zip(model_name, product_url):
            product_url = url.get_attribute("href")
            new_data = {
                "Model Name": model.text,
                "Product url": product_url,
                "Software Name": vendor,
            }
            self.list_of_dict.append(new_data)
        return self.list_of_dict
        
    def get_vendor_name(self):
        """Helper function to retrieve the vendor name"""
        vendor_element = self.driver.find_element(By.XPATH, "//h1[@class='ge-category-hero__details--title']")
        return vendor_element.text 

    def scrape_data(self, url, output_filename):
        """scrape_data function collects the data
        : returns dataframe and CSV file"""
        self.open_url(url)

        #Close the pop up which appear on the screen
        pop_up = self.driver.find_element(By.XPATH, "//*[@id='_evidon_banner']")
        button = self.click_element_by_xpath(pop_up,".//button")

        #Path upto the link from which data is to be scraped
        Products = self.click_element_by_xpath(self.driver,"//*[@id='primary-navigation-item-0']/span")
        main_div = self.driver.find_element(By.XPATH, "//div[@class='menu-content-container-center']")
        Ultrasound = self.click_element_by_xpath(self.driver, "//div[@id='secondTierMenuLink_0']/div[2]/p") 
        
        main_link_div = main_div.find_element(By.XPATH, "//div[@class='menu-content-container-items second-tier expand']/div[2]")
        links = self.click_element_by_xpath(main_link_div,".//a[1]/p" )
        vendor_1 = self.get_vendor_name()
        main_ultrasound_container = self.driver.find_element(By.XPATH, "//div[@class='sub-specialty-data']/div[1]/div")
        model_name = main_ultrasound_container.find_elements(By.XPATH, ".//div/div[2]/div/p")  
        product_url_tag = main_ultrasound_container.find_elements(By.XPATH, ".//div/p/a") 
        #Appending data into list of dict
        self.common_dict(model_name, product_url_tag, vendor_1)

        #Path upto the link from which data is to be scraped
        Products = self.click_element_by_xpath(self.driver,"//*[@id='primary-navigation-item-0']/span")
        main_div = self.driver.find_element(By.XPATH, "//div[@class='menu-content-container-center']")
        Ultrasound = self.click_element_by_xpath(self.driver, "//div[@id='secondTierMenuLink_0']/div[2]/p")

        main_link_div = main_div.find_element(By.XPATH, "//div[@class='menu-content-container-items second-tier expand']/div[2]")
        vscan_handheld = self.click_element_by_xpath(main_link_div, ".//a[9]/p") 
        vendor_2 = self.get_vendor_name()
        main_vscan_container = self.driver.find_element(By.XPATH, "//div[@class='mdc-layout-grid__inner sub-specialty-data-section']")
        model_name_vscan = main_vscan_container.find_elements(By.XPATH, ".//div/div/div[2]")
        product_url_tag_vscan = main_vscan_container.find_elements(By.XPATH, ".//div/div/p/a")
        self.common_dict(model_name_vscan, product_url_tag_vscan, vendor_2)

        """Collecting data into dataframe and converting dataframe to CSV file"""
        df = pd.DataFrame(self.list_of_dict)
        df.to_csv(output_filename, index=False)
        print(df)
        self.driver.close()
        return df

#Calling the function to scrape the data
scraper = Ultrasound()
scraper.scrape_data(scraper.url, r"Tutorial\CSV\Ultrasound.csv")
