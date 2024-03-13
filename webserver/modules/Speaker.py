from transformers import AutoTokenizer, AutoModelForCausalLM


class Speaker:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.model = self.model.to("cpu")

    def talk(self):
        # nah what the hell is happening here
        user_input = input("Human: ")
        inputs = self.tokenizer(user_input, return_tensors="pt")
        inputs = {k: v.to("cpu") for k, v in inputs.items()}
        outputs = self.model.generate(
            **inputs,
            max_length=inputs["input_ids"].shape[1] + 20,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        response_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("Assistant:", response_text.removeprefix(user_input))

        print(response_text)

    def get_key(self):
        try:
            file = open("keys.txt", "r")
            keys = file.read()
            key_change = str(keys).rfind("~")
            return keys[key_change + 1 :]
        except Exception as e:
            print("Failed to read key:", e)
