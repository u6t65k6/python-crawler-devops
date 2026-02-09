import csv
from pathlib import Path
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

def load_test_plan():
    test_url_list = []
    PLAN_FILE = Path(__file__).parent / 'plan' / 'general.csv'
    with open(PLAN_FILE, newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        # 🔑 關鍵：清理欄位名稱
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        for row in reader:
            test_url_list.append(row["url"].strip())
    return test_url_list

def generate_report(list_test_report, filename=f"report-{timestamp}.csv"):
    # 欄位順序
    fieldnames = ["item", "response", "snapshot"]
    # 開啟檔案（寫入模式）
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # 寫入欄位名稱（標題）
        writer.writeheader()
        # 寫入每一列資料
        for row in list_test_report:
            writer.writerow(row)
    print(f"報告已生成：{filename}")
    


