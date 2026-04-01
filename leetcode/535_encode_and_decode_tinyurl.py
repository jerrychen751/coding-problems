import random
import string

class Codec:
    def __init__(self, length: int = 8):
        self.short_urls: dict[str, str] = {}
        self.length = length

    def encode(self, longUrl: str) -> str:
        """Encodes a URL to a shortened URL.
        """
        short_url = "".join(random.choices(string.ascii_letters + string.digits, k=self.length))
        self.short_urls[short_url] = longUrl
        return short_url

    def decode(self, shortUrl: str) -> str:
        """Decodes a shortened URL to its original URL.
        """
        return self.short_urls[shortUrl]

# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(url))