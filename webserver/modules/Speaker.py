from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login


class Speaker:
    def __init__(self):
        login()
        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
        self.model = AutoModelForCausalLM.from_pretrained(
            "google/gemma-2b", device_map="auto"
        )
        input_text = "Write me a poem about Machine Learning."
        input_ids = self.tokenizer(input_text, return_tensors="pt")
        input_ids = input_ids.to(self.model.device)
        outputs = self.model.generate(**input_ids)
        print(self.tokenizer.decode(outputs[0]))
