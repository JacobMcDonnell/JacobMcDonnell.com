import redis

class DB:
    def __init__(self, host='localhost', port=6379):
        self.db = redis.Redis(host=host, port=port, decode_responses=True)

    def add_article(r, article):
        r.db.hset(f"articles:{article['url']}", mapping=article)

    def get_article(r, name):
        return r.db.hgetall(f"articles:{name}")

    def get_all_articles(r):
        keys = r.get_all_articles_keys()
        return [r.db.hgetall(key) for key in keys]

    def get_all_articles_keys(r):
        return [key for key in r.db.scan_iter(f"articles:*")]

    def get_all_keys(r):
        return [key for key in r.db.scan_iter("*")]

