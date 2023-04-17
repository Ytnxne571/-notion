notion_properties = {
    "Idea": {
        "title": [
            {
                "text": {"content": ""},
            }
        ]
    },
    "Date": {
        "date": {
            "start": "",
        }
    },
    "Category": {
        "select": {
            "name": "",
        }
    },
    "Book Title": {
        "title": [
            {
                "text": {"content": ""},
            }
        ]
    },
    "Book Cover": {
        "url": ""
    }
}

def get_ideas(idea_list):
    """从列表或数据库中检索想法"""
    ideas = []

    # 遍历想法列表或数据库，并将每个想法添加到 ideas 列表中
    for idea in idea_list:
        ideas.append(idea)

    # 处理每个想法并插入到 Notion 中
    for idea in ideas:
        insert_to_notion(idea, database_id)

def insert_to_notion(idea, database_id):
    """将想法插入到 Notion 中"""
    parent = {
        "database_id": database_id,
        "type": "database_id"
    }

    # 为新的想法页面设置属性
    properties = notion_properties.copy()
    properties["Idea"]["title"][0]["text"]["content"] = idea["text"]
    properties["Date"]["date"]["start"] = idea["date"]
    properties["Category"]["select"]["name"] = idea["category"]
    properties["Book Title"]["title"][0]["text"]["content"] = idea["book_title"]
    properties["Book Cover"]["url"] = idea["book_cover"]

    # 在 Notion 中创建一个新的页面，并设置上述属性
    client.pages.create(parent=parent, properties=properties)

def get_idea_list(filename):
    """从文件或数据库中检索想法列表"""
    ideas = []

    # 从文件或数据库中读取想法，并将每个想法添加到 ideas 列表中
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        ideas = [idea for idea in data]

    # 处理每个想法并插入到 Notion 中
    for idea in ideas:
        insert_to_notion(idea, database_id)

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument("notion_token", help="Notion API token")
    parser.add_argument("database_id", help="Notion database ID")
    parser.add_argument("filename", help="File name of the idea list")
    options = parser.parse_args()
    notion_token = options.notion_token
    database_id = options.database_id
    filename = options.filename

    # 创建 Notion 客户端对象
    client = Client(auth=notion_token, log_level=logging.DEBUG)

    # 获取想法列表并插入到 Notion 中
    get_idea_list(filename)

    # 自定义 Notion 数据库属性
    notion_properties["Idea"]["title"][0]["text"]["content"] = "Custom Idea property"
    notion_properties["Date"]["date"]["start"] = "Custom date"
    notion_properties["Category"]["select"]["name"] = "Custom category"
    notion_properties["Book Title"]["title"][0]["text"]["content"] = "Custom book title"
    notion_properties["Book Cover"]["url"] = "https://example.com/book_cover.jpg"
