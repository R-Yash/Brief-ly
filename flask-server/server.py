from flask import Flask,jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_news_from_db():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, title, image, summary FROM news")
    rows = cursor.fetchall()
    conn.close()
    
    news_list = []
    for row in rows:
        news = {
            "id": row[0],
            "title": row[2],
            "content": row[4],
            "image": row[3],
            "link": row[1]
        }
        news_list.append(news)
    return news_list

@app.route('/news', methods=['GET'])
def news():
    news_list = get_news_from_db()
    return jsonify(news_list)

if __name__ == '__main__':
    app.run(debug=True)