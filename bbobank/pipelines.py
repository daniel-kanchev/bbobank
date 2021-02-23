from itemadapter import ItemAdapter
import sqlite3


class DatabasePipeline:
    # Database setup
    conn = sqlite3.connect('bbobank.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute(""" CREATE TABLE IF NOT EXISTS articles 
        (title text, content text) """)

    def process_item(self, item, spider):
        self.c.execute("""SELECT * FROM articles WHERE title = ?""",
                       (item.get('title'), ))
        duplicate = self.c.fetchall()
        if len(duplicate):
            return item
        print(f"New entry added: {item['title']}")

        # Insert values
        self.c.execute("INSERT INTO articles (title, content)"
                       " VALUES (?,?)", (item.get('title'), item.get('content')))
        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
