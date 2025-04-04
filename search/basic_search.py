from elasticsearch import Elasticsearch


# Connect to Elasticsearch
es = Elasticsearch('http://localhost:9200')

# Check connection
if es.ping():
    print("Connected to Elasticsearch!")
else:
    print("Connection failed.")

def create_index(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f"Index '{index_name}' created!")


def index_book(index_name, book_id, title, content):
    doc = {
        'title': title,
        'content': content
    }
    es.index(index=index_name, id=book_id, body=doc)
    print(f"Indexed book: {title}")

# searching the books on matching the query to content
def search_books(index_name, query):
    search_body = {
        'query': {
            'match': {
                'content': query
            }
        }
    }
    response = es.search(index=index_name, body=search_body)
    return response['hits']['hits']




if __name__ == '__main__':
    index_name = 'books'
    
    # Step 1: Create index
    create_index(index_name)
    
    # Step 2: Add books
    books = [
        {'id': 1, 'title': 'Harry Potter', 'content': 'A young wizard named Harry goes to Hogwarts.'},
        {'id': 2, 'title': 'The Lord of the Rings', 'content': 'A hobbit named Frodo embarks on an adventure to destroy the One Ring.'},
        {'id': 3, 'title': 'Sherlock Holmes', 'content': 'Detective Sherlock Holmes solves mysterious cases in London.'}
    ]
    
    for book in books:
        index_book(index_name, book['id'], book['title'], book['content'])
    
    # Step 3: Search books
    query = input("Enter a word to search in books: ")
    results = search_books(index_name, query)
    
    print("\nSearch Results:")
    for result in results:
        print(f"Title: {result['_source']['title']}, Score: {result['_score']}")
