import requests

api = "http://api.quotable.io/random"
quotes = []
quote_number = 0


def preload_quotes():
    global quotes

    print("Loading new quotes!")
    for i in range(10):
        random_quote = requests.get(api).json()
        quote_content = random_quote["content"]
        quote_author = random_quote["author"]
        quote = quote_content + "\n\n" + "By " + quote_author
        quotes.append(quote)


preload_quotes()

