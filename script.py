import requests
import time

def get_data():
    data = []
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]

    for url in urls:
        r = requests.get(url)
        if r.status_code == 200:
            data.append(r.json())
        else:
            print("error")
        time.sleep(1)

    return data

def process_data(data):
    result = []
    for item in data:
        if "title" in item:
            result.append(item["title"])
    return result

if __name__ == "__main__":
    d = get_data()
    titles = process_data(d)
    print(titles)
