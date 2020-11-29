import os
import time
from .db import MyModel
from transformers import MarianMTModel, MarianTokenizer

translated_db = os.getenv("DB_TRANSLATED")

translator = MyModel(translated_db, 2)

models = {}

model_name = f"Helsinki-NLP/opus-mt-he-ru"
he2ru_tokenizer = MarianTokenizer.from_pretrained(model_name)
he2ru_model = MarianMTModel.from_pretrained(model_name)

models[model_name] = (he2ru_model, he2ru_tokenizer)

model_name = f"Helsinki-NLP/opus-mt-en-he"
en2he_tokenizer = MarianTokenizer.from_pretrained(model_name)
en2he_model = MarianMTModel.from_pretrained(model_name)

models[model_name] = (en2he_model, en2he_tokenizer)