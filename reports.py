import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

def load_test_plan():
    test_url_list = []
    PLAN_FILE = Path(__file__).parent / 'plan' / 'general.csv'
    try:
        with open(PLAN_FILE, newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            for row in reader:
                url = row.get("url", "").strip()
                if url:  # 過濾空值
                    test_url_list.append(url)
    except FileNotFoundError:
        print(f"找不到檔案：{PLAN_FILE}")
    except KeyError as e:
        print(f"CSV 檔案缺少必要欄位：{e}")
    
    return test_url_list

def generate_report(list_test_report: List[Dict[str, str]]) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"report-{timestamp}.csv"
    output_path = Path(__file__).parent / 'report' / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    # 欄位順序
    fieldnames = ["item", "response", "snapshot"]
    try:
        with open(output_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(list_test_report)  # 可以直接用 writerows
        
        print(f" 報告已生成：{filename}")
    except Exception as e:
        print(f" 寫入報告時發生錯誤：{e}")
    


