from dotenv import load_dotenv
import os
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from reports import load_test_plan, generate_report
from apis.req import api_test
from crawler import snapshot, webelement_check
import traceback

load_dotenv()
CHROME_PATH = os.getenv('CHROME_PATH')
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')


@contextmanager
def chrome_driver():
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_PATH
    options.add_argument("--disable-gpu")
    options.add_argument('--headless=new')
    options.add_argument("--window-size=1920,1080")
    
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        yield driver  
    finally:
        driver.quit()  

def create_test_report(driver, url, index):
    try:
        driver.get(url)
        element_check_result = webelement_check(driver, url)
        if element_check_result['all_present']:
            print(f"前端元素檢查：{element_check_result['page_name']}全部元素存在")
        else:
            print(f"前端元素檢查：{element_check_result['page_name']}缺少元素 :{element_check_result['missing_elements']}")
        item, response = api_test(url)
        snapshot_path = snapshot(driver, index)
        return {
            'item': item,
            'response': response,
            'snapshot': snapshot_path
        }
    except Exception as e:
        print(f"測試 URL {index},{url} 發生錯誤: {e}")
        traceback.print_exc()
        return {
            'item': url,
            'response': 'ERROR', 
            'snapshot': ''
        }
        

def main():
    with chrome_driver() as driver:
        list_test_report = []
        test_url = load_test_plan()
        for index, url in enumerate(test_url):
            print(f"[{index+1}/{len(test_url)}] 正在載入頁面: {url}")
            report = create_test_report(driver, url, index)   
            list_test_report.append(report)
    generate_report(list_test_report)

if __name__ == '__main__':
    main()
