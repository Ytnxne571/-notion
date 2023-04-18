from pprint import pprint
from datetime import datetime
from notion_client import Client
from notion.block import TextBlock

# Notion API key，需要修改为自己的 API key
NOTION_API_KEY = "secret_VMxqT0pKsZMmziMrDD9FOR87uFz1dsMSngOOlGZ4UAT"

# Notion 数据库名称，需要修改为自己的数据库名称
NOTION_DATABASE_NAME = "My Book Database"

# Notion 父页面 ID，需要修改为自己的页面 ID
NOTION_PARENT_PAGE_ID = "7a5161c68a784b2a9f3bf5ae54998d6b"

# 书籍信息，需要修改为自己的书籍信息
book_name = "The Great Gatsby"
book_cover = "https://images-na.ssl-images-amazon.com/images/I/51TtT1wK0jL._SX331_BO1,204,203,200_.jpg"
book_author = "F. Scott Fitzgerald"
book_publisher = "Scribner"
book_pubdate = datetime(1925, 4, 10).strftime('%Y-%m-%d')
progress_percent = 50

# 初始化 Notion 客户端
notion = Client(auth=NOTION_API_KEY)

# 检查是否已经存在名为 NOTION_DATABASE_NAME 的数据库
result = notion.search(query=NOTION_DATABASE_NAME, filter={"property": "object", "value": "database"}).get("results")
if len(result) == 0:
    # 如果不存在，则创建一个新的数据库
    new_database = {
        "Name": {
            "title": [{"text": {"content": NOTION_DATABASE_NAME}}]
        },
        "Description": {
            "rich_text": [{"text": {"content": "This is my book database."}}]
        }
    }
    database = notion.databases.create(parent={"page_id": NOTION_PARENT_PAGE_ID}, properties=new_database)
    print(f"Created database \"{NOTION_DATABASE_NAME}\" with ID \"{database.id}\"")
else:
    # 如果已经存在，则使用该数据库
    database = notion.databases.retrieve(database_id=result[0].id)
    print(f"Retrieved database \"{NOTION_DATABASE_NAME}\" with ID \"{database.id}\"")

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
