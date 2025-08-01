from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
import vertexai
import os


# not used currently
def create_rag_corpus(project_id, display_name, location="us-central1"):
    """
    Create a new RAG corpus in Vertex AI.
    Returns the corpus object.
    """
    vertexai.init(project=project_id, location=location)
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model="publishers/google/models/text-embedding-005"
        )
    )
    rag_corpus = rag.create_corpus(
        display_name=display_name,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        ),
    )
    return rag_corpus


def upload_transcript_file_to_corpus(project_id, corpus_name, transcript_file, display_name, description=None, location="us-central1"):
    """
    Upload a local transcript file to a RAG corpus.
    Returns the RagFile object.
    """
    vertexai.init(project=project_id, location=location)
    rag_file = rag.upload_file(
        corpus_name=corpus_name,
        path=transcript_file,
        display_name=display_name,
        description=description or "Transcript file uploaded via API",
    )
    print("IIDDD:   ",rag_file.display_name)
    return rag_file


# not used currently
def vertex_rag_retrieval_query(project_id, corpus_name, query, top_k=3, location="us-central1", vector_distance_threshold=0.5):
    """
    Retrieve context from a RAG corpus for a given query.
    Returns the retrieval response object.
    """
    vertexai.init(project=project_id, location=location)
    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=top_k,
        filter=rag.Filter(vector_distance_threshold=vector_distance_threshold),
    )
    response = rag.retrieval_query(
        rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
        text=query,
        rag_retrieval_config=rag_retrieval_config,
    )
    return response


def vertex_rag_generate_answer(project_id, corpus_name, query, top_k=3, location="us-central1", vector_distance_threshold=0.5, model_name="gemini-2.0-flash-001"):
    """
    Generate an answer using Gemini and RAG retrieval tool.
    Returns the generated answer string.
    """
    vertexai.init(project=project_id, location=location)
    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=top_k,
        filter=rag.Filter(vector_distance_threshold=vector_distance_threshold),
    )
    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[rag.RagResource(rag_corpus=corpus_name)],
                rag_retrieval_config=rag_retrieval_config,
            ),
        )
    )
    rag_model = GenerativeModel(
        model_name=model_name,
        tools=[rag_retrieval_tool],
        generation_config={"temperature": 0.1}
    )
    response = rag_model.generate_content(query)
    return response.text

