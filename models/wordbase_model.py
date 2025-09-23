class WordBaseModel:
    def __init__(self, word):
        self.spelling = word["account"]
        self.type = word["type"]
        self.meanings = word["meanings"]
        self.examples = word["examples"]
