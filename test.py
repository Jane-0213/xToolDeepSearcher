import logging
import os
from deepsearcher.offline_loading import load_from_local_files, load_from_website
from deepsearcher.online_query import query
from deepsearcher.configuration import Configuration, init_config

# Suppress unnecessary logging from third-party libraries
logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    # Step 1: Initialize configuration
    config = Configuration()

    # Configure Vector Database and Docling providers
    config.set_provider_config("vector_db", "Milvus", {})
    config.set_provider_config("file_loader", "DoclingLoader", {})
    config.set_provider_config("web_crawler", "DoclingCrawler", {})

    # Apply the configuration
    init_config(config)

    # # Step 2a: Load data from a local file using DoclingLoader
    # local_file = "your_local_file_or_directory"
    # local_collection_name = "DoclingLocalFiles"
    # local_collection_description = "Milvus Documents loaded using DoclingLoader"
    #
    # print("\n=== Loading local files using DoclingLoader ===")
    #
    # try:
    #     load_from_local_files(
    #         paths_or_directory=local_file,
    #         collection_name=local_collection_name,
    #         collection_description=local_collection_description,
    #         force_new_collection=True
    #     )
    #     print(f"Successfully loaded: {local_file}")
    # except ValueError as e:
    #     print(f"Validation error: {str(e)}")
    # except Exception as e:
    #     print(f"Error: {str(e)}")
    #
    # print("Successfully loaded all local files")

    # Step 2b: Crawl URLs using DoclingCrawler
    urls = [
        # Markdown documentation files
        "https://milvus.io/docs/quickstart.md",
        "https://milvus.io/docs/overview.md",
        # PDF example - can handle various URL formats
        "https://arxiv.org/pdf/2408.09869",
    ]
    web_collection_name = "DoclingWebCrawl"
    web_collection_description = "Milvus Documentation crawled using DoclingCrawler"

    print("\n=== Crawling web pages using DoclingCrawler ===")

    load_from_website(
        urls=urls,
        collection_name=web_collection_name,
        collection_description=web_collection_description,
        force_new_collection=True
    )
    print("Successfully crawled all URLs")

    # Step 3: Query the loaded data
    question = "What is Milvus?"
    result = query(question)
    print(result)


if __name__ == "__main__":
    main()