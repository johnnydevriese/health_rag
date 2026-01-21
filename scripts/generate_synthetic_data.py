import os
import json
import logfire
from deepeval.synthesizer import Synthesizer
from app.core.config import settings
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import Document

# Configure logfire defensively
if settings.LOGFIRE_TOKEN:
    logfire.configure(token=settings.LOGFIRE_TOKEN)

def generate_synthetic_data():
    """Generate synthetic evaluation data from Medicare documents."""
    
    # 1. Load documents (same as IngestService)
    markdown_path = "app/gen-ai-homework-assignment/input/medicare_comparison.md"
    if not os.path.exists(markdown_path):
        print(f"Error: Markdown file not found at {markdown_path}")
        return

    with open(markdown_path, "r") as f:
        content = f.read()

    # Simple parsing to get chunks for the synthesizer
    parser = MarkdownNodeParser()
    nodes = parser.get_nodes_from_documents([Document(text=content)])
    texts = [node.get_content() for node in nodes]

    print(f"Loaded {len(texts)} chunks. Generating synthetic test cases...")

    # 2. Setup Synthesizer with Google GenAI
    print(f"Using model: {settings.LLM_MODEL}")
    
    from app.services.evaluation import GeminiGenAI
    
    model = GeminiGenAI(
        model_name=settings.LLM_MODEL,
        api_key=settings.GEMINI_API_KEY
    )
    
    synthesizer = Synthesizer(model=model)

    # 3. Generate Goldens
    # Pass texts as a list of lists of contexts
    contexts = [[text] for text in texts[:2]]
    
    goldens = synthesizer.generate_goldens_from_contexts(
        contexts=contexts,
        max_goldens_per_context=2
    )

    # 4. Save results
    os.makedirs("eval_data", exist_ok=True)
    output_path = "eval_data/synthetic_test_cases.json"
    
    # Goldens can be serialized to JSON
    synthesizer.save_as(file_type="json", directory="eval_data")
    
    print(f"Successfully generated and saved synthetic test cases to eval_data/")

if __name__ == "__main__":
    generate_synthetic_data()
