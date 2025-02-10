import os
from google import genai

class GeminiEmbeddings:
    def __init__(self, api_key: str, model: str = 'text-embedding-004'):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def embed_query(self, query: str) -> list[float]:
        response = self.client.models.embed_content(model=self.model, contents=query)
        return response.embeddings[0].values

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        all_embeddings = []
        for text in texts:
            response = self.client.models.embed_content(model=self.model, contents=text)
            embedding_vector = response.embeddings[0].values
            all_embeddings.append(embedding_vector)
        return all_embeddings

    def __call__(self, text: str) -> list[float]:
        return self.embed_query(text)

if __name__ == "__main__":
    embeddings = GeminiEmbeddings(api_key="Gemini-api-key")
    sample_embedding = embeddings.embed_query("Test embedding")
    print("Sample Embedding:", sample_embedding[:5])