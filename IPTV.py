import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import re

guangxi = "https://fofa.info/result?qbase64=ImlwdHYvbGl2ZS96aF9jbi5qcyIgJiYgY291bnRyeT0iQ04iICYmIHJlZ2lvbj0iR3Vhbmd4aSBaaHVhbmd6dSI%3D" #广西

def process_url(url):
# 创建一个Chrome WebDriver实例
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
# 使用WebDriver访问网页
driver.get(url) # 将网址替换为你要访问的网页地址
time.sleep(10)
# 获取网页内容
page_content = driver.page_source

# 关闭WebDriver
driver.quit()

# 查找所有符合指定格式的网址
pattern = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+" # 设置匹配的格式，如http://8.8.8.8:8888
urls_all = re.findall(pattern, page_content)
urls = list(set(urls_all)) # 去重得到唯一的URL列表
for url in urls:
print(url)
# 遍历网址列表，获取JSON文件并解析
results = []
for url in urls:
try:
# 发送GET请求获取JSON文件，设置超时时间为5秒
json_url = f"{url}/iptv/live/1000.json?key=txiptv"
response = requests.get(json_url, timeout=3)
json_data = response.json()

# 解析JSON文件，获取name和url字段
for item in json_data['data']:
if isinstance(item, dict):
name = item.get('name')
urlx = item.get('url')
urld = f"{url}{urlx}"

if name and urlx:
# 删除特定文字
name = name.replace("中央", "CCTV")
name = name.replace("高清", "")
name = name.replace("HD", "")
name = name.replace("标清", "")
name = name.replace("频道", "")
name = name.replace("-", "")
name = name.replace(" ", "")
name = name.replace("PLUS", "+")
name = name.replace("(", "")
name = name.replace(")", "")
name = name.replace("CCTV1综合", "CCTV1")
name = name.replace("CCTV2财经", "CCTV2")
name = name.replace("CCTV3综艺", "CCTV3")
name = name.replace("CCTV4国际", "CCTV4")
name = name.replace("CCTV4中文国际", "CCTV4")
name = name.replace("CCTV5体育", "CCTV5")
name = name.replace("CCTV6电影", "CCTV6")
name = name.replace("CCTV7军事", "CCTV7")
name = name.replace("CCTV7军农", "CCTV7")
name = name.replace("CCTV7国防军事", "CCTV7")
name = name.replace("CCTV8电视剧", "CCTV8")
name = name.replace("CCTV9记录", "CCTV9")
name = name.replace("CCTV9纪录", "CCTV9")
name = name.replace("CCTV10科教", "CCTV10")
name = name.replace("CCTV11戏曲", "CCTV11")
name = name.replace("CCTV12社会与法", "CCTV12")
name = name.replace("CCTV13新闻", "CCTV13")
name = name.replace("CCTV新闻", "CCTV13")
name = name.replace("CCTV14少儿", "CCTV14")
name = name.replace("CCTV15音乐", "CCTV15")
name = name.replace("CCTV16奥林匹克", "CCTV16")
name = name.replace("CCTV17农业农村", "CCTV17")
name = name.replace("CCTV5+体育赛视", "CCTV5+")
name = name.replace("CCTV5+体育赛事", "CCTV5+")
results.append(f"{name},{urld}")
except requests.exceptions.RequestException as e:
print(f"Failed to process JSON for URL {json_url}. Error: {str(e)}")
continue
except json.JSONDecodeError as e:
print(f"Failed to parse JSON for URL {url}. Error: {str(e)}")
continue

return results
def save_results(results, filename):
# 将结果保存到文本文件
with open(filename, "w", encoding="utf-8") as file:
for result in results:
file.write(result + "\n")
print(result)

# 处理第1个URL
results_hebei = process_url(guangxi)
save_results(results_guangxi, "guangxi.txt")

# 合并文件内容
file_contents = []
file_paths = ["guangxi.txt"] # 替换为实际的文件路径列表
for file_path in file_paths:
with open(file_path, 'r', encoding="utf-8") as file:
content = file.read()
file_contents.append(content)

# 写入合并后的文件
with open("IPTV.txt", "w", encoding="utf-8") as output:
output.write('\n'.join(file_contents))