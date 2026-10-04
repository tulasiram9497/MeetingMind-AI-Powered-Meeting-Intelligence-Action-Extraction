from __future__ import annotations

import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import VECTOR_DIR


class EmbeddingStore:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.index_path = VECTOR_DIR / 'index.faiss'
        self.metadata_path = VECTOR_DIR / 'metadata.json'

    def embed_text(self, text: str) -> np.ndarray:
        vector = self.model.encode([text], normalize_embeddings=True)
        return np.asarray(vector, dtype='float32')

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        vectors = self.model.encode(texts, normalize_embeddings=True)
        return np.asarray(vectors, dtype='float32')

    def build_index(self, texts: list[str]) -> tuple[faiss.Index, list[dict[str, object]]]:
        vectors = self.embed_documents(texts)
        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)
        metadata = [{'text': text} for text in texts]
        return index, metadata

    def save_index(self, index: faiss.Index, metadata: list[dict[str, object]]) -> None:
        faiss.write_index(index, str(self.index_path))
        self.metadata_path.write_text(json.dumps(metadata, ensure_ascii=False), encoding='utf-8')

    def load_index(self) -> tuple[faiss.Index | None, list[dict[str, object]]]:
        if not self.index_path.exists():
            return None, []
        index = faiss.read_index(str(self.index_path))
        metadata = json.loads(self.metadata_path.read_text(encoding='utf-8')) if self.metadata_path.exists() else []
        return index, metadata

    def similarity_search(self, query: str, top_k: int = 5) -> list[dict[str, object]]:
        index, metadata = self.load_index()
        if index is None or not metadata:
            return []
        vector = self.embed_text(query)
        scores, indices = index.search(vector, min(top_k, len(metadata)))
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            result = metadata[int(idx)]
            result['score'] = float(score)
            results.append(result)
        return results
