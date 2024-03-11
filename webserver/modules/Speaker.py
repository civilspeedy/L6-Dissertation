from transformers import GemmaModel


class Speaker:
    def __init__(self):
        self.model = GemmaModel.from_pretrained("google/gemma-2b")

    def talk(self):
        while True:
            user_input = input(">>")
            if user_input == "end":
                break
            else:
                response = self.model.generate(user_input)
                print(response)
