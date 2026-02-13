from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Dict, List

def snapshot(driver, path):
    filename = f"{path}.png"   #str(path).replace('/', '_').replace(':', '_')
    output_path = Path(__file__).parent / 'screenshot' / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(output_path)
    return Path('screenshot') / filename

ELEMENT_CONFIGS = {
    'signup': [
        {'by': By.ID, 'value': "email", 'info': '電子信箱輸入欄位', 'condition': EC.visibility_of_element_located},
        {'by': By.ID, 'value': "username", 'info': '使用者名稱輸入欄位', 'condition': EC.visibility_of_element_located},
        {'by': By.ID, 'value': "password", 'info': '密碼輸入欄位', 'condition': EC.visibility_of_element_located},
        {'by': By.ID, 'value': "cfm_password", 'info': '確認密碼輸入欄位', 'condition': EC.visibility_of_element_located},
        {'by': By.TAG_NAME, 'value': "button", 'info': '註冊按鈕', 'condition': EC.element_to_be_clickable}
    ],
    'signin': [
        {'by': By.ID, 'value': "email", 'info': '電子信箱輸入欄位', 'condition': EC.visibility_of_element_located},
        {'by': By.ID, 'value': "password", 'info': '密碼輸入欄位', 'condition': EC.visibility_of_element_located},
        {'by': By.TAG_NAME, 'value': "button", 'info': '登入按鈕', 'condition': EC.element_to_be_clickable}
    ]
}

PAGE_NAMES = {
    'signup': '註冊頁面',
    'signin': '登入頁面'
}

def check_element_exists(driver, element_config: Dict, wait_time: int = 5) -> bool:
    try:
        WebDriverWait(driver, wait_time).until(
            element_config['condition']((element_config['by'], element_config['value']))
        )
        return True
    except:
        return False

def webelement_check(driver, url: str, wait_time: int = 5) -> Dict:
    
    page_type = next((key for key in ELEMENT_CONFIGS if key in url), None)
    
    if not page_type:
        print(f"無法識別頁面類型: {url}")
        return {
            'page_name': 'unknown',
            'all_present': False,
            'missing_elements': [],
            'total_elements': 0
        }
    
    page_name = PAGE_NAMES[page_type]
    elements = ELEMENT_CONFIGS[page_type]
    
    missing_elements: List[str] = []
    
    for element in elements:
        if not check_element_exists(driver, element, wait_time):
            print(f"在{page_name}中缺少{element['info']}")
            missing_elements.append(element['info'])
    
    return {
        'page_name': page_name,
        'all_present': len(missing_elements) == 0,
        'missing_elements': missing_elements,
        'total_elements': len(elements)
    }
