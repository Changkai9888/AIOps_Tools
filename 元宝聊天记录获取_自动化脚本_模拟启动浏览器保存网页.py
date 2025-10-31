#模拟启动浏览器保存网页，适用于保存动态网页。

url = "https://yb.tencent.com/s/tSkAxretIfTb"
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup  # 导入BeautifulSoup用于解析HTML
import time

# 设置Chrome选项（关键：无头模式）
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # 启用无头模式，浏览器在后台运行
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 自动管理ChromeDriver
service = Service(ChromeDriverManager().install())

# 初始化浏览器（此时不会弹出浏览器窗口）
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 访问网页
    driver.get(url)
    # 等待页面加载（可根据需要调整时间或使用更智能的等待条件）
    time.sleep(3)
    
    # 获取渲染后的完整页面HTML源码
    page_html = driver.page_source
    # 保存到文件
    with open('saved_page_dynamic.html', 'w', encoding='utf-8') as f:
        f.write(page_html)
    print("动态渲染后的网页已成功保存为 saved_page_dynamic.html")
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(page_html, 'html.parser')
    
    # 提取整个页面的纯文本内容
    # `separator` 参数指定段落间的分隔符，`strip=True` 用于去除多余空白
    text_content = soup.get_text(separator='\n', strip=True)
    
    # 将文本内容保存到txt文件
    output_filename = "网页内容.txt"
    with open(output_filename, "w", encoding="utf-8") as text_file:
        text_file.write(text_content)
    
    print(f"成功！网页文本内容已保存到 '{output_filename}'")
    
finally:
    # 关闭浏览器
    driver.quit()
