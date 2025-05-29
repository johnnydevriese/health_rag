### Build a simple Retrieval-Augmented Generation (RAG) System

**Time Limit**: 2-3 hours

**Objective:** Design a simplified RAG pipeline that retrieves context from a knowledge base and uses it to generate answers to user queries.

**Problem Statement**

You are tasked with building a simple RAG system. You are given a collection of documents (in this case, a single document comparing Original Medicare and Medicare Advantage) and a set of user queries. Your task is to:

1.  Index the document into a searchable format.
    
2.  Retrieve relevant context for a given query.
    
3.  Generate answers using a language model (LLM) conditioned on the retrieved context. For the sake of this exercise, let's assume our context window has a maximum of 80 tokens.
    

**Requirements**

1.  Document Processing & Indexing
    

-   **Input**: A directory input/ containing a markdown file: `medicare_comparison.md`.
    
-   **Task**:
	-   Split the document into chunks. 
	    
	-   Generate embeddings for each chunk using a pretrained model (e.g., all-MiniLM-L6-v2).
	    
	-   Store embeddings how you best see fit  
      
2.  Query Processing & Retrieval

-   **Input**: A directory input/ containing a JSON file `queries.json`.
    
-   **Task**:
    
	-   For each query, retrieve the most relevant document chunks
	    
	-   Handle edge cases (e.g., no relevant chunks found).  

3.  Answer Generation

-   **Task**:
    
	-   Use an LLM (e.g., GPT-3.5-turbo, Llama 3, or any Hugging Face model) to generate answers conditioned on the retrieved context.
	    
	-   Format answers for user and store answer in JSON output.
    
4.  Output
    
-   Application should return results to user and save to output/answers.json. The format should be:
```
    {
	    "query_id":  "Q1",
	    "query_text":  "Can I see any doctor with Original Medicare?",
	    "answer":  "<answer>",
	    "source_chunks":  ["<chunk_id_1>",  "<chunk_id_2>"],
	    "source_text": ["<supporting_text_1", "supporting_text_2"]
    }
```
  
-   Your application should be idempotent in practice, not perfectly idempotent.
    
-   Your application should handle hallucinations reasonably well and should not include information that’s not included in the provided source document.

**Expectations**  

-   Clover primarily uses Python, but your application can be written with language/libraries of your choosing. Be prepared to explain why you chose them.  
    
-   Be prepared to run your application and demonstrate its capabilities. We’ll ask you to index the document and query it with all the questions provided in the queries.json. We’ll want to see the supporting chunks used when responding to queries.  
    
-   Your application should handle other questions and remain grounded to the source document provided. It should not respond with information that’s not grounded.  
      
-   Please bring up with your interviewers any gaps, trade offs, limitations of your software. We like to see that you are thinking about all the ways you can improve your design.
