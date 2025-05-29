import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def semantic_chunking(text, nlp, chunk_size=3, similarity_threshold=0.75):
    """
    Splits text into semantically coherent chunks using sentence embeddings.

    Args:
        text (str): The input text to chunk.
        nlp: A pre-initialized spaCy NLP model.
        chunk_size (int): The maximum number of sentences per chunk.
        similarity_threshold (float): The minimum cosine similarity between sentences
            within a chunk.

    Returns:
        list: A list of text chunks.
    """
    doc = nlp(text)
    sentences = list(doc.sents)
    embeddings = [sent.vector for sent in sentences]  # Get sentence embeddings

    chunks = []
    current_chunk = []
    current_embedding = np.zeros(embeddings[0].shape) # Initialize an empty embedding
    
    for i, (sentence, embedding) in enumerate(zip(sentences, embeddings)):
        if not current_chunk:
            current_chunk.append(sentence.text)
            current_embedding = embedding
        else:
            # Calculate cosine similarity between the current sentence and the accumulated chunk embedding
            similarity = cosine_similarity([current_embedding], [embedding])[0][0]
            
            if len(current_chunk) < chunk_size and similarity >= similarity_threshold:
                # Add sentence to the current chunk
                current_chunk.append(sentence.text)
                # update the current embedding.
                current_embedding = np.mean([current_embedding, embedding], axis=0)
            else:
                # Start a new chunk
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence.text]
                current_embedding = embedding

    if current_chunk:
        chunks.append(" ".join(current_chunk))  # Add the last chunk

    return chunks

def main():
    """
    Main function to run the semantic chunking example.
    """
    # Load a spaCy model with word vectors.  Make sure you have downloaded a model.
    # You might need to run: python -m spacy download en_core_web_md
    nlp = spacy.load("en_core_web_md")

    # Example text (replace with your actual text)
    text = """
    This is a longer text for testing the semantic chunking.  It contains several sentences.
    The sentences are about different topics, to demonstrate how the chunking works.
    We want to group sentences that are semantically similar.
    This is another sentence on a similar topic. And this one too.
    However, this sentence is completely different. It talks about something else.
    So, it should be in a separate chunk.  This is the end of the example.
    Semantic chunking is very useful for RAG.
    """

    # Perform semantic chunking
    chunks = semantic_chunking(text, nlp)

    # Print the chunks
    print("Semantic Chunks:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:")
        print(chunk)
        print("-" * 20)


if __name__ == "__main__":
    main()

# taken from gemini 2.5 pro 