class FakeDB:

    def __init__(self):
        self.storage = {}

    async def save(self, key, value):
        self.storage[key] = value

    async def load(self, key):
        return self.storage[key]

    