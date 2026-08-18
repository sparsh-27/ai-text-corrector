from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class ModernCorrector:
    def __init__(self):
        model_name = "vennify/t5-base-grammar-correction"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        # Use GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        
    def correct(self, text: str) -> str:
        input_text = "grammar: " + text
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=128,
            num_beams=4,
            early_stopping=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    corrector = ModernCorrector()
    print(corrector.correct("I am writting a leter to you"))
