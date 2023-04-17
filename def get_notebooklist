import argparse
import json
import logging
import time
from notion_client import Client
import requests
from requests.utils import cookiejar_from_dict
from http.cookies import SimpleCookie
from datetime import datetime

WEREAD_URL = "https://weread.qq.com/"
WEREAD_NOTEBOOKS_URL = "https://i.weread.qq.com/user/notebooks"
WEREAD_BOOKMARKLIST_URL = "https://i.weread.qq.com/book/bookmarklist"

# Notion数据库的属性
notion_properties = {
    "MarkText": {"title": [{"type": "text", "text": {"content": ""}}]},
    "BookId": {"rich_text": [{"type": "text", "text": {"content": ""}}]},
    "BookmarkId": {"rich_text": [{"type": "text", "text": {"content": ""}}]},
    "BookName": {"rich_text": [{"type": "text", "text": {"content": ""}}]},
    "Type": {"select": {"name": ""}},
    "Cover": {"files": [{"type": "external", "name": "Cover", "external": {"url": ""}}]},
    "Date": {"date": {"start": "", "time_zone": "Asia/Shanghai"}},
    "Style": {"select": {"name": ""}}
}

def parse_cookie_string(cookie_string):
    """将cookie字符串解析为字典格式"""
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    cookies_dict = {}
    cookiejar = None
    for key, morsel in cookie.items():
        cookies_dict[key] = morsel.value
        cookiejar = cookiejar_from_dict(
            cookies_dict, cookiejar=None, overwrite=True
        )
    return cookiejar

def get_hot(书名, 封面, 书籍ID):
    """获取划线"""
    params = dict(bookId=书籍ID)
    r = session.get(WEREAD_BOOKMARKLIST_URL, params=params)
    if r.ok:
        datas = r.json()["updated"]
        for data in datas:
            if not check(data["bookmarkId"]):
                insert_to_notion(书名, 封面, data)
            else:
                print("已经插入过了")

def check(bookmarkId):
    """检查是否已经插入过"""
    filter = {
        "property": "BookmarkId",
        "rich_text": {
            "equals": bookmarkId
        }
    }
    response = client.databases.query(database_id=database_id, filter=filter)
    return len(response["results"]) > 0

def insert_to_notion(书名, 封面, data):
    time.sleep(0.3)
    """插入到Notion"""
    parent = {
        "database_id": database_id,
        "type": "database_id"
    }

    # 更新Notion数据库的属性
    properties = notion_properties.copy()
    properties["MarkText"]["title"][0]["text"]["content"] = data["markText"]
    properties["BookId"]["rich_text"][0]["text"]["content"] = data["bookId"]
    properties["BookmarkId"]["rich_text"][0]["text"]["content"] = data["bookmarkId"]
    properties["BookName"]["rich_text"][0]["text"]["content"] = 书名
    properties["Type"]["select"]["name"] = str(data["type"])
    properties["Cover"]["files"][0]["external"]["url"] = 封面
    
    # 如果data中包含createTime属性，则将其转换为日期格式
    if "createTime" in data:
        date = datetime.utcfromtimestamp(data["createTime"]).strftime("%Y-%m-%d %H:%M:%S")
        properties["Date"]["date"]["start"] = date
    if "style" in data:
        properties["Style"]["select"]["name"] = str(data["style"])
    
    client.pages.create(parent=parent, properties=properties)

def get_notebooklist():
    """获取笔记本列表"""
    r = session.get(WEREAD_NOTEBOOKS_URL)
    books = []

    # 将笔记本列表保存到文件中
    with open("notebooks.json", "w", encoding="utf-8") as f:
        f.write(r.text)
    if r.ok:
        data = r.json()
        books = data["books"]
        for book in books:
            title = book["book"]["title"]
            cover = book["book"]["cover"]
            bookId = book["book"]["bookId"]
            get_hot(title, cover, bookId)

if __name__ == "main":
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("weread_cookie", help="微信读书的cookie")
    parser.add_argument("notion_token", help="Notion的token")
    parser.add_argument("database_id", help="Notion的数据库ID")
    options = parser.parse_args()
    weread_cookie = options.weread_cookie
    database_id = options.database_id
    notion_token = options.notion_token

    # 创建会话对象和Notion客户端对象
    session = requests.Session()
    session.cookies = parse_cookie_string(weread_cookie)
    client = Client(auth=notion_token, log_level=logging.DEBUG)
    session.get(WEREAD_URL)

    # 获取笔记本列表并处理
    get_notebooklist()
    
    # 可自定义修改Notion数据库的属性
    notion_properties["MarkText"]["title"][0]["text"]["content"] = "自定义MarkText属性"
    notion_properties["BookId"]["rich_text"][0]["text"]["content"] = "自定义BookId属性"
    notion_properties["BookmarkId"]["rich_text"][0]["text"]["content"] = "自定义BookmarkId属性"
    notion_properties["BookName"]["rich_text"][0]["text"]["content"] = "自定义BookName属性"
    notion_properties["Type"]["select"]["name"] = "自定义Type属性"
    notion_properties["Cover"]["files"][0]["external"]["url"] = "自定义Cover属性的URL"
    notion_properties["Date"]["date"]["start"] = "自定义Date属性的日期"
    notion_properties["Style"]["select"]["name"] = "自定义Style属性"
