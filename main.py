from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from apis.req import api_test
from reports import load_test_plan, generate_report
from crawler import snapshot

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless=new')

driver = webdriver.Chrome(service = service, options = options)

# 產生測試報告的資料結構
list_test_report = []

# 讀取測試計畫
test_url = load_test_plan()

# 執行前、後端測試
for index in range(len(test_url)):
    dict_test_report = {"item":"", "response":"", "snapshot":""}
    
    driver.get(test_url[index])
    dict_test_report["snapshot"] = snapshot(driver, index)
    dict_test_report["item"], dict_test_report["response"] = api_test(test_url[index])
    list_test_report.append(dict_test_report)

# 產生測試報告
generate_report(list_test_report)
