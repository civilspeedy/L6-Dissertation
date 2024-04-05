from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login


class Speaker:
    def __init__(self):
        login()
        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b")
        self.model = AutoModelForCausalLM.from_pretrained(
            "google/gemma-2b", device_map="auto"
        )

        self.model.config.hidden_activation = "gelu_pytorch_tanh"

        input_text = "hello"
        input_ids = self.tokenizer(input_text, return_tensors="pt")
        input_ids = input_ids.to(self.model.device)
        outputs = self.model.generate(
            **input_ids,
            max_new_tokens=200,
            early_stopping=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        print(self.tokenizer.decode(outputs[0]))
