import torch
from transformers import AutoTokenizer, TFAutoModelForCausalLM


class Speaker:
    def __init__(self):
        self.model = "gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model)
        self.model_instance = TFAutoModelForCausalLM.from_pretrained(
            self.model)
        self.model_instance.config.pad_token_id = self.model_instance.config.eos_token_id

    def talk(self, input):
        model_inputs = self.tokenizer([input], return_tensors="tf")
        model_generate = self.model_instance.generate(
            **model_inputs, do_sample=True, seed=((42, 0)))
        print("out: ", self.tokenizer.decode(model_generate[0]))
