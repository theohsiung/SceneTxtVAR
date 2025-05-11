from transformers import T5Tokenizer, T5ForConditionalGeneration
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xl", cache_dir="./weights")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl", cache_dir="./weights")