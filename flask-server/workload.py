import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import sqlite3

def fetch_html(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_main_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all('figure')

def extract_article_links(articles):
    links = []
    for art in articles:
        try:
            link = art.find('a').get('href')
            if link:
                links.append(link)
        except AttributeError:
            continue
    return links

def fetch_article_details(session, link):
    try:
        r = session.get(link)
        r.raise_for_status()
        return BeautifulSoup(r.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching article {link}: {e}")
        return None

def parse_article_details(sp):
    article_details = {'headline': '', 'text': '', 'image': ''}
    try:
        article_details['headline'] = sp.find('h1').text
        article_details['text'] = sp.find('div', {'class': '_s30J clearfix'}).text
        article_details['image'] = sp.find('section').find('img').get('src')
    except AttributeError:
        pass
    return article_details

def summarize_article(summarizer, text):
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
    return " ".join(s['summary_text'].strip() for s in summary)

def split_into_chunks(text, max_chunk_size=500):
    if text == "":
        return []
    
    text = text.replace('.', '.<eos>').replace('!', '!<eos>').replace('?', '?<eos>')
    sentences = text.split('<eos>')
    chunks, current_chunk = [], []

    for sentence in sentences:
        if len(current_chunk) + len(sentence.split()) <= max_chunk_size:
            current_chunk.extend(sentence.split())
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = sentence.split()
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def process_news_articles(articles, summarizer, processed_urls):
    news_data = []
    session = requests.Session()

    for article in articles:
        if article in processed_urls:
            continue

        article_page = fetch_article_details(session, article)
        if not article_page:
            continue

        article_details = parse_article_details(article_page)
        chunks = split_into_chunks(article_details['text'])
        
        article_summary = [summarize_article(summarizer, chunk) for chunk in chunks]
        summarized_text = " ".join(article_summary)
        
        news_data.append({
            'url': article,
            'title': article_details['headline'],
            'image': article_details['image'],
            'summary': summarized_text
        })
    
    return news_data

def store_in_database(news_data, db_name="news.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, image TEXT, summary TEXT)''')
    
    for news in news_data:
        try:
            c.execute('''INSERT INTO news (url, title, image, summary) VALUES (?, ?, ?, ?)''', 
                      (news['url'], news['title'], news['image'], news['summary']))
        except sqlite3.IntegrityError:
            print('URL already exists in the database. Skipping.....')
            continue
    
    conn.commit()
    conn.close()

def get_processed_urls(db_name="news.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (id INTEGER PRIMARY KEY, url TEXT UNIQUE, title TEXT, image TEXT, summary TEXT)''')
    
    c.execute('''SELECT url FROM news''')
    urls = c.fetchall()
    
    conn.close()
    return [url[0] for url in urls]

def main():
    url = "https://timesofindia.indiatimes.com/"
    html = fetch_html(url)
    if not html:
        return
    
    articles = parse_main_page(html)
    article_links = extract_article_links(articles)
    
    processed_urls = get_processed_urls()
    
    summarizer = pipeline("summarization", model='sshleifer/distilbart-cnn-12-6')
    summarized_news = process_news_articles(article_links, summarizer, processed_urls)
    
    store_in_database(summarized_news)

if __name__ == "__main__":
    main()
