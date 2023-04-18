from pprint import pprint
from datetime import datetime
from notion_client import Client
from notion.block import TextBlock

# Notion API key
NOTION_API_KEY = ""

# Notion 数据库名称
NOTION_DATABASE_NAME = "My Book Database"

# 初始化 Notion 客户端
notion = Client(auth=NOTION_API_KEY)

# 检查是否已经存在名为 NOTION_DATABASE_NAME 的数据库
results = notion.search(query=NOTION_DATABASE_NAME, filter={"property": "object", "value": "database"}).get("results")
if len(results) == 0:
    # 如果不存在，则创建一个新的数据库
    database = notion.databases.create(parent={"page_id": NotionParentPageID}, title=[{"type": "text", "text": {"content": NOTION_DATABASE_NAME}}])
    print(f"Created database \"{NOTION_DATABASE_NAME}\" with ID \"{database.id}\"")
else:
    # 如果已经存在，则使用该数据库
    database = notion.databases.retrieve(database_id=results[0].id)
    print(f"Retrieved database \"{NOTION_DATABASE_NAME}\" with ID \"{database.id}\"")

# 获取书籍信息
book_name = ""
book_cover = ""
book_author = ""
book_publisher = ""
book_pubdate = ""
progress_percent = 0

# 在 Notion 中检查这本书是否已经存在
existing_page = None
result = notion.databases.query(
    **{
        "database_id": database.id,
        "filter": {
            "property": "Name",
            "title": {
                "equals": book_name,
            },
        },
    }
)

# 如果这本书已经存在，则更新页面信息
if len(result["results"]) > 0:
    existing_page = result["results"][0]
else:
    # 如果这本书还不存在，则创建新页面并添加其信息
    new_page = {
        "Name": {
            "title": [{"text": {"content": book_name}}]
        },
        "Cover": {
            "files": [{"name": book_name, "external": {"url": book_cover}}]
        },
        "Author": {
            "rich_text": [{"text": {"content": book_author}}]
        },
        "Publisher": {
            "rich_text": [{"text": {"content": book_publisher}}]
        },
        "PubDate": {
            "date": {"start": book_pubdate}
        },
        "Progress": {
            "number": progress_percent
        }
    }
    existing_page = notion.pages.create(parent={"database_id": database.id}, properties=new_page)

print(f"Synchronized book {book_name} to Notion database!")
