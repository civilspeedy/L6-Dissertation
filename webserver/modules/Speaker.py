class Speaker:
    def __init__(self):
        self.key = self.get_key()

    def get_key(self):
        try:
            file = open("keys.txt", "r")
            keys = file.read()
            key_change = str(keys).rfind("~")
            return keys[key_change + 1 :]
        except Exception as e:
            print("Failed to read key:", e)
