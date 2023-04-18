import requests
from pprint import pprint
from datetime import datetime
from notion_client import Client

# 微信读书 cookie
COOKIE = "wr_fp=3140426081; wr_gid=234723305; wr_vid=436256338; wr_pf=2; wr_rt=web%40eCqhqxVmZmZN2cOmWcr_AL; wr_localvid=92c3206081a00be5292cdb1; wr_name=%D0%90%D0%BD%D1%82%D0%BE%D0%BD; wr_avatar=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FDYAIOgq83eq7YJ6yJNJt1qSE4JZyJdHNZRDzbGUXdicmqEYibOktLWyunf1EUUv9skD7CwhSeo2TgdMIEJYkw0pA%2F132; wr_gender=0"

# Notion API key
NOTION_API_KEY = "secret_VMxqT0pKsZMmziMrDD9FOR87uFz1dsMSngOOlGZ4UAT"

# Notion 数据库 ID
NOTION_DATABASE_ID = "7a5161c68a784b2a9f3bf5ae54998d6b"

# 获取微信读书书籍详情
def get_book_details(book_uri):
    url = f"https://i.weread.qq.com/book/info?uri={book_uri}&t=1641660490267"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Cookie": COOKIE,
    }
    response = requests.get(url, headers=headers)
    book_detail = response.json()["data"]
    return book_detail

# 获取微信读书笔记
def get_reading_notes(book_uri):
    url = f"https://i.weread.qq.com/review/list?pageSize=1000&targetUri={book_uri}&order=desc&t=1641667056555"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Cookie": COOKIE,
    }
    response = requests.get(url, headers=headers)
    notes = response.json()["data"]["items"]
    return notes

# 初始化 Notion 客户端
notion = Client(auth=NOTION_API_KEY)

# 打开指定的 Notion 数据库
database = notion.databases.retrieve(database_id=NOTION_DATABASE_ID)

# 获取微信读书书籍详情
book_uri = ""
book_detail = get_book_details(book_uri)

# 在 Notion 中检查这本书是否已经存在
existing_page = None
result = notion.databases.query(
    **{
        "database_id": NOTION_DATABASE_ID,
        "filter": {
            "property": "Name",
            "title": {
                "equals": book_detail["name"],
            },
        },
    }
)

# 如果这本书已经存在，则更新页面信息
if len(result["results"]) > 0:
    existing_page = result["results"][0]
    existing_page_title = book_detail["name"]
    existing_page_cover = book_detail["cover"]
    existing_page_author = book_detail["author"]
    existing_page_publisher = book_detail["publisher"]
    existing_page_isbn = book_detail["isbn"]
    existing_page_pubdate = datetime.strptime(book_detail["pubdate"], "%Y-%m-%d").date().isoformat()
else:
    # 如果这本书还不存在，则创建新页面并添加其信息
    new_page = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": book_detail["name"]
                    }
                }]
        },
        "Cover": {
            "files": [{"name": book_detail["name"], "external": {"url": book_detail["cover"]}}],
        },
        "Author": {
            "title": [
                {"text": {"content": book_detail["author"]}}
            ]
        },
        "Publisher": {
            "title": [
                {"text": {"content": book_detail["publisher"]}}
            ]
        },
        "ISBN": {
            "title": [
                {"text": {"content": book_detail["isbn"]}}
            ]
        },
        "PubDate": {
            "date": {
                "start": datetime.strptime(book_detail["pubdate"], "%Y-%m-%d").date().isoformat()
            }
        }
    }

    existing_page = notion.pages.create(parent={"database_id": NOTION_DATABASE_ID}, properties=new_page)

# 获取微信读书笔记
notes = get_reading_notes(book_uri)

# 添加书籍信息
existing_page.properties["Name"].title[0].text.content = existing_page_title
existing_page.properties["Cover"].files = [{"name": existing_page_title, "external": {"url": existing_page_cover}}]
existing_page.properties["Author"].title[0].text.content = existing_page_author
existing_page.properties["Publisher"].title[0].text.content = existing_page_publisher
existing_page.properties["ISBN"].title[0].text.content = existing_page_isbn
existing_page.properties["PubDate"].date.start = existing_page_pubdate

# 添加读书笔记
for note in notes:
    if "PageIndex" in note:
        # 页面笔记
        page_index = note["PageIndex"]
        note_content = note["Content"]
        new_page = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": note_content
                        }
                    }]
            },
            "Page": {
                "relation": [
                    {
                        "id": page_index
                    }
                ]
            }
        }
        notion.pages.create(parent={"page_id": existing_page.id}, properties=new_page)
    elif "ChapterTitle" in note:
        # 章节笔记
        chapter_title = note["ChapterTitle"]
        note_content = note["Content"]
        new_page = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": note_content
                        }
                    }]
            },
            "Chapter": {
                "relation": [
                    {
                        "title": [
                            {
                                "text": {
                                    "content": chapter_title
                                }
                            }]
                    }
                ]
            }
        }
        notion.pages.create(parent={"page_id": existing_page.id}, properties=new_page)
    elif "BookReview" in note:
        # 书评
        book_review = note["BookReview"]
        new_page = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": "Book Review"
                        }
                    }]
            },
            "Content": {
                "rich_text": [
                    {
                        "text": {
                            "content": book_review,
                            "link": None
                        }
                    }
                ]
            }
        }
        notion.pages.create(parent={"page_id": existing_page.id}, properties=new_page)
    else:
        # 划线笔记
        highlight_text = note["Content"]
        highlight_location = note["Location"]
        new_page = {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": highlight_text
                        }
                    }]
            },
            "Highlight": {
                "select": {
                    "name": "Yes"
                }
            },
            "Location": {
                "rich_text": [
                    {
                        "text": {
                            "content": highlight_location
                        }
                    }
                ]
            }
        }
        notion.pages.create(parent={"page_id": existing_page.id}, properties=new_page)

print("Synchronized book details and reading notes to Notion!")
