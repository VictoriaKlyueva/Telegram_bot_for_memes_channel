import random
import torch
from transformers import pipeline
from config import HF_USERNAME, HF_MODEL_NAME, TOKENIZER_PATH
from utils.utils import get_prompt, text_post_processing


device = "cuda" if torch.cuda.is_available() else "cpu"

# Making pipeline for transformer
pipe = pipeline(
    'text-generation',
    model=f"{HF_USERNAME}/{HF_MODEL_NAME}",
    tokenizer=TOKENIZER_PATH,
    temperature=1.2,
    top_k=50,
    top_p=0.9,
    do_sample=True,
    max_new_tokens=55,
    truncation=True,
    device=0 if device == "cuda" else -1
)

print("Текстовая модель загружена")


def generate_text():
    while True:
        prompt = get_prompt()
        result = random.choice(text_post_processing(pipe(prompt)[0]['generated_text'])[:2])

        if len(result) > len(prompt):
            break
        else:
            print("Генерация продолжается")

    print("Prompt:", prompt, "Output:", result)

    if len(result) > 20 and len(result.split()) == 1:
        result = result[:20]

    return result
