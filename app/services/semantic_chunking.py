import numpy as np
from typing import List, Dict, Any
import voyageai
from ..core.config import settings
import logfire

class SemanticChunker:
    """Enterprise-grade semantic chunker using VoyageAI embeddings."""

    def __init__(self, buffer_size: int = 1, breakpoint_percentile_threshold: float = 95):
        """
        Initialize the semantic chunker.
        
        Args:
            buffer_size: Number of sentences to combine on each side of a break for context
            breakpoint_percentile_threshold: The percentile of distance changes that will be considered a break
        """
        self.voyage_client = voyageai.Client(api_key=settings.VOYAGE_API_KEY)
        self.buffer_size = buffer_size
        self.breakpoint_percentile_threshold = breakpoint_percentile_threshold

    def _split_into_sentences(self, text: str) -> List[str]:
        """Simple sentence splitter. For enterprise grade, we use regex or a library like nltk/spacy."""
        # Split by periods, question marks, exclamation marks followed by a space
        import re
        sentences = re.split(r'(?<=[.!?]) +', text)
        return [s.strip() for s in sentences if s.strip()]

    def _combine_sentences(self, sentences: List[str], buffer_size: int) -> List[str]:
        """Combines sentences with a sliding window to capture more context for embeddings."""
        combined_sentences = []
        for i in range(len(sentences)):
            # Combine sentences around index i
            start = max(0, i - buffer_size)
            end = min(len(sentences), i + buffer_size + 1)
            combined = " ".join(sentences[start:end])
            combined_sentences.append(combined)
        return combined_sentences

    def chunk(self, text: str) -> List[str]:
        """
        Perform semantic chunking on the given text.
        """
        with logfire.span("semantic_chunking_execution", text_length=len(text)):
            sentences = self._split_into_sentences(text)
            if len(sentences) < 2:
                return [text]

            # 1. Generate embeddings for combined sentences (with buffer for context)
            combined = self._combine_sentences(sentences, self.buffer_size)
            
            with logfire.span("generating_embeddings_for_chunking"):
                embeddings_response = self.voyage_client.embed(
                    texts=combined,
                    model="voyage-3",
                    input_type="document"
                )
                embeddings = np.array(embeddings_response.embeddings)

            # 2. Calculate distances between adjacent embeddings
            distances = []
            for i in range(len(embeddings) - 1):
                # Cosine distance = 1 - cosine similarity
                similarity = np.dot(embeddings[i], embeddings[i+1]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i+1])
                )
                distances.append(1 - similarity)

            # 3. Identify breakpoints based on distance percentile
            if not distances:
                return [text]
            
            breakpoint_distance_threshold = np.percentile(distances, self.breakpoint_percentile_threshold)
            indices_above_threshold = [i for i, d in enumerate(distances) if d > breakpoint_distance_threshold]

            # 4. Create chunks based on breakpoints
            chunks = []
            start_index = 0
            for index in indices_above_threshold:
                # Group sentences from start_index to index (inclusive)
                chunk = " ".join(sentences[start_index:index + 1])
                chunks.append(chunk)
                start_index = index + 1
            
            # Add the last remaining part
            if start_index < len(sentences):
                chunk = " ".join(sentences[start_index:])
                chunks.append(chunk)

            return chunks
