import argparse
import json
import logging
import time
from datetime import datetime
from http.cookies import SimpleCookie

import requests
from notion_client import Client
from requests.utils import cookiejar_from_dict

# 声明一些常量
WEREAD_URL = "https://weread.qq.com/"
WEREAD_NOTEBOOKS_URL = "https://i.weread.qq.com/user/notebooks"
WEREAD_BOOKMARKLIST_URL = "https://i.weread.qq.com/book/bookmarklist"

def parse_cookie_string(cookie_string):
    """将微信读书的 cookie 字符串解析为字典格式"""
    cookie = SimpleCookie()
    cookie.load(cookie_string)
    cookies_dict = {}
    cookiejar = None
    for key, morsel in cookie.items():
        cookies_dict[key] = morsel.value
        cookiejar = cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
    return cookiejar

def check(bookmark_id):
    """检查 Notion 数据库中是否已经存在相同的书签"""
    filter = {
        "property": "BookmarkId",
        "rich_text": {"equals": bookmark_id}
    }
    response = client.databases.query(database_id=database_id, filter=filter)
    return len(response["results"]) > 0

def insert_to_notion(book_name, cover, data):
    """将书签插入到 Notion 数据库中"""
    time.sleep(0.3)
    parent = {"database_id": database_id, "type": "database_id"}

    # 更新 Notion 数据库的属性
    properties = notion_properties.copy()
    properties["MarkText"]["title"][0]["text"]["content"] = data["markText"]
    properties["BookId"]["rich_text"][0]["text"]["content"] = data["bookId"]
    properties["BookmarkId"]["rich_text"][0]["text"]["content"] = data["bookmarkId"]
    properties["BookName"]["rich_text"][0]["text"]["content"] = book_name
    properties["Type"]["select"]["name"] = str(data["type"])
    properties["Cover"]["files"][0]["name"] = "Cover"
    properties["Cover"]["files"][0]["external"]["url"] = cover

    # 如果 data 中包含 createTime 属性，则将其转换为日期格式
    if "createTime" in data:
        date = datetime.utcfromtimestamp(data["createTime"]).strftime("%Y-%m-%d %H:%M:%S")
        properties["Date"]["date"]["start"] = date
    if "style" in data:
        properties["Style"]["select"]["name"] = str(data["style"])

    client.pages.create(parent=parent, properties=properties)

def get_hot(book_name, cover, book_id):
    """获取热门书签"""
    params = dict(bookId=book_id)
    r = session.get(WEREAD_BOOKMARKLIST_URL, params=params)
    if r.ok:
        datas = r.json()["updated"]
        for data in datas:
            # 如果书签已经存在，则跳过
            if not check(data["bookmarkId"]):
                insert_to_notion(book_name, cover, data)
            else:
                print("书签已经存在")

def get_notebooklist():
    """获取笔记本列表"""
    r = session.get(WEREAD_NOTEBOOKS_URL)
    if r.ok:
        data = r.json()
        books = data["books"]
        for book in books:
            book_name = book["book"]["title"]
            cover = book["book"]["cover"]
            book_id = book["book"]["bookId"]
            get_hot(book_name, cover, book_id)

if __name__ == "__main__":
    # 定义可供修改的变量
    # Microsof Notion API  token
    notion_token = "<NOTION_TOKEN>"

    # 微信读书 cookie，注意 cookie 中的双引号需要使用转义符号
    weread_cookie = "<COOKIE>"

    # Notion 数据库 id
    database_id = "<DATABASE_ID>"

    # 定义 Notion 数据库的属性
    notion_properties = {
        "MarkText": {"title": [{"type": "text", "text": {"content": "书签文本"}}]},
        "BookId": {"rich_text": [{"type": "text", "text": {"content": "书籍 ID"}}]},
        "BookmarkId": {"rich_text": [{"type": "text", "text": {"content": "书签 ID"}}]},
        "BookName": {"rich_text": [{"type": "text", "text": {"content": "书名"}}]},
        "Type": {"select": {"name": "类型"}}},
        "Cover": {"files": [{"type": "external", "name": "封面", "external": {"url": ""}}]},
        "Date": {"date": {"start": "", "time_zone": "Asia/Shanghai"}},
        "Note": {"rich_text": [{"type": "text", "text": {"content": "笔记"}}]},
        "Style": {"select": {"name": ""}}
    }

    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("weread_cookie", help="微信读书的 cookie")
    parser.add_argument("notion_token", help="Notion 的 token")
    parser.add_argument("database_id", help="Notion 的数据库 ID")
    options = parser.parse_args()
    weread_cookie = options.weread_cookie
    notion_token = options.notion_token
    database_id = options.database_id

    # 创建会话对象和 Notion 客户端对象
    session = requests.Session()
    session.cookies = parse_cookie_string(weread_cookie)
    client = Client(auth=notion_token, log_level=logging.DEBUG)
    session.get(WEREAD_URL)

    # 获取笔记本列表并处理
    get_notebooklist()

    # 可自定义修改 Notion 数据库的属性
    # for key in notion_properties.keys():
    #     notion_properties[key]["title"][0]["text"]["content"] = f"自定义 {key} 属性"
