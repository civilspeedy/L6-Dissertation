import keras
import keras_nlp
import kaggle


class Speaker:
    # might not be arm64 compatible yet
    def __init__(self):
        self.model = keras_nlp.models.GemmaCausalLM.from_preset("gemma_instruct_2b_en")
        print(self.model.generate("hello", max_length=30))
