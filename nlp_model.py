# nlp_model.py

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

# NLP Modelini ve Tokenizer'ı yükle
# Model yüklendikten sonra bir daha yüklenmemesi için bu kısım globalde tutulur.
print("NLP modelini yüklüyor...")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
model = AutoModel.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
print("NLP modeli başarıyla yüklendi.")

def get_embedding(text):
    """
    Bir metni sayısal vektöre (embedding) dönüştürür.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        model_output = model(**inputs)
    # Pooling: Mean pooling across the sequence dimension
    sentence_embedding = model_output.last_hidden_state.mean(dim=1).squeeze().numpy()
    return sentence_embedding