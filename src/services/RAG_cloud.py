from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
import vertexai
import os

def get_rag_lecture_chat_model(project_id, corpus_name, rag_file_id, top_k, location, vector_distance_threshold, model_name):
    """
    Returns a GenerativeModel for chat, configured for a specific RAG file.
    """
    
    vertexai.init(project=project_id, location=location)
    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=top_k,
        filter=rag.Filter(vector_distance_threshold=vector_distance_threshold),
    )
    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[rag.RagResource(rag_corpus=corpus_name, rag_file_ids=[str(rag_file_id)])],
                rag_retrieval_config=rag_retrieval_config,
            ),
        )
    )
    rag_model = GenerativeModel(
        model_name=model_name,
        tools=[rag_retrieval_tool],
        generation_config={"temperature": 0.1}
    )

    return rag_model

def upload_transcript_file_to_corpus(project_id, corpus_name, transcript_text_path, display_name, description=None, location="us-central1"):
    """
    Upload transcript text to RAG corpus and return the file resource.
    """
    vertexai.init(project=project_id, location=location)
    rag_file = rag.upload_file(
        corpus_name=corpus_name,
        path=transcript_text_path,
        display_name=display_name,
        description=description or "Transcript file uploaded via API",
    )
    return rag_file
