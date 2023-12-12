from neural_cherche import models, rank, retrieve
import torch
import config
import json
import utils

def get_relevant_tools(query,retriever,ranker,ranker_documents_embeddings,documents,k=10):

    batch_size = 32
    tool_info = json.load(open(config.TOOLS_PATH,'r'))

    retriever_queries_embeddings = retriever.encode_queries(
        queries=[query],
    )

    ranker_queries_embeddings = ranker.encode_queries(
        queries=[query],
        batch_size=batch_size,
    )
    candidates = retriever(
        queries_embeddings=retriever_queries_embeddings,
        k=1000,
    )
    results = ranker(
        documents=candidates,
        queries_embeddings=ranker_queries_embeddings,
        documents_embeddings=ranker_documents_embeddings,
        k=100,
        batch_size=32,
    )

    relevant_tools = []

    # Iterate through each inner list
    for i, inner_list in enumerate(results, start=1):
        print(i)
        # Sort the inner list by similarity in descending order
        sorted_inner_list = sorted(inner_list, key=lambda x: x['similarity'], reverse=True)
        
        # Extract the top 10 eretriever_documents_embeddings,lements
        top_k_elements = sorted_inner_list[:k]

        # List to store results for the current inner list
        current_results = []

        # Print the corresponding elements from the tool_info using the 'id'
        for j, element in enumerate(top_k_elements, start=1):
            element_id = element['id']
            # Corrected line to extract element_name
            element_name = next(x['text'].split(":")[0] for x in documents if x['id'] == element_id)
            tool_details = next((tool for tool in tool_info if tool['tool_name'] == element_name), None)
            if tool_details:
                current_results.append(tool_details)
        
        # Add the list for the current inner list to the overall results dictionary
        relevant_tools += current_results

    return relevant_tools

def load_model():


    device = "cuda" if torch.cuda.is_available() else "cpu"

    retriever = retrieve.TfIdf(
        key="id",
        on=["text"],
    )

    model = models.ColBERT(
        model_name_or_path=config.RETRIEVER_CHECKPOINT,
        device=device
    )

    ranker = rank.ColBERT(
        key="id",
        on=["text"],
        model=model
    )

    batch_size = 32

    _,documents = utils.load_and_preprocess_tools_data(config.TOOLS_PATH)

    retriever_documents_embeddings = retriever.encode_documents(
        documents=documents,
    )

    ranker_documents_embeddings = ranker.encode_documents(
        documents=documents,
        batch_size=batch_size,
    )

    retriever.add(
        documents_embeddings=retriever_documents_embeddings,
    )

    return retriever,ranker,ranker_documents_embeddings,documents

