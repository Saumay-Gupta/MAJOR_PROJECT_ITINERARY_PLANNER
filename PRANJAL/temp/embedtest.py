from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")

emb = model.encode("Romantic scenic honeymoon trip in Goa")

print(len(emb))

v1 = model.encode("Romantic lake sunset")
v2 = model.encode("Beautiful lake with sunset view")
v3 = model.encode("Airport terminal building")

def cosine(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

print("Romantic vs Lake:", cosine(v1,v2))
print("Romantic vs Airport:", cosine(v1,v3))

