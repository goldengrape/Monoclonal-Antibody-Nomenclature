import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

# @st.experimental_singleton
# def get_driver():
#     return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# @st.experimental_singleton
def init() -> webdriver.Chrome:
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # driver = webdriver.Chrome()
    # return driver

def first_query(driver: webdriver.Chrome, query_string: str) -> None:
    driver.get("https://poca-public.fda.gov/")
    # wait for the checkbox to be visible
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//mat-checkbox[@id='mat-checkbox-1']/label/span")))
    driver.find_element(By.XPATH, "//mat-checkbox[@id='mat-checkbox-1']/label/span").click()
    # driver.find_element(By.CSS_SELECTOR, ".mat-checkbox-inner-container").click()

    driver.find_element(By.XPATH, "(//button[@type='button'])[2]").click()
    # wait for the search box to be visible
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "mat-input-0")))
    driver.find_element(By.ID, "mat-input-0").click()
    driver.find_element(By.ID, "mat-input-0").send_keys(query_string)    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("abcd inputted")
    # wait for the table to be visible
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((
        By.XPATH, "//a/span/span")))
    print("table visible")
    driver.find_element(By.XPATH, "//a/span/span").click()
    print("export button clicked")
    # /html/body/app-root/div[2]/app-name-search/div[4]/table[2]/tbody 
    # 获取表格内容
    table=driver.find_element(By.XPATH, "/html/body/app-root/div[2]/app-name-search/div[4]/table[2]/tbody")
    return table




def other_query(driver: webdriver.Chrome, query_string: str) -> None:
    driver.get("https://poca-public.fda.gov/")
    # wait for the search box to be visible
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "mat-input-0")))
    driver.find_element(By.ID, "mat-input-0").click()
    driver.find_element(By.ID, "mat-input-0").send_keys(query_string)    
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    print("abcd inputted")
    # wait for the table to be visible
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((
        By.XPATH, "//a/span/span")))
    print("table visible")
    driver.find_element(By.XPATH, "//a/span/span").click()
    print("export button clicked")
    # /html/body/app-root/div[2]/app-name-search/div[4]/table[2]/tbody 
    # 获取表格内容
    table=driver.find_element(By.XPATH, "/html/body/app-root/div[2]/app-name-search/div[4]/table[2]/tbody")
    return table

def get_table(table, sep=",") -> None:
    rows=table.find_elements(By.TAG_NAME, "tr")
    # 打印表格内容
    data=[]
    for row in rows[:3]:
        cells=row.find_elements(By.TAG_NAME, "td")
        row_data={}
        row_data["name"]=cells[0].text
        row_data["score"]=cells[1].text
        data.append(row_data)
    return data

def main(query_list, item_sep=";", col_sep=","):
    driver = init()
    df = {}
    for i in range(len(query_list)):
        q = query_list[i]
        query_method = first_query if i == 0 else other_query
        table=query_method(driver, q)
        data = get_table(table, col_sep)
        # data = item_sep.join(data)
        df[q] = data
    driver.quit()
    return df

if __name__ == "__main__":
    input = sys.argv[1:]
    query_list = input
    df = main(query_list)
    print(df)
    # browser = init()
    # first_query(browser, "innov")
