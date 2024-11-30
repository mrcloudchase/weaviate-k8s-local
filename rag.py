import weaviate
from weaviate.classes.config import Configure
from openai import OpenAI
import dotenv
import os
import json
import requests

# Load environment variables
dotenv.load_dotenv()

# Set the X-OpenAI-API-Key header
headers = {
    "X-OpenAI-API-Key": os.getenv("OPENAI_API_KEY")
}

# Connect to local Weaviate instance running in Docker Compose
client = weaviate.connect_to_local(
    port=32360,
    grpc_port=32361,
    headers=headers
)

# Test Readiness of Weaviate
try:
    client.is_ready()
    print("Weaviate is ready!")
except Exception as e:
    print(f"Weaviate is not ready: {e}")
    exit(1)

# Check if the collection exists and if not, create it
try:                
    if not client.collections.exists("Question"):
        # Print a message to indicate that the collection is being created
        print("Creating collection...")
        # Create a new collection in Weaviate instance
        client.collections.create(
            # Name of the collection
            name="Question",
            # Vectorizer configuration for the collection
            vectorizer_config=Configure.Vectorizer.text2vec_openai(
            # Name of the OpenAI model to use for vectorization
                model="text-embedding-3-small"
            ),
            # Generative model configuration for the collection
            generative_config=Configure.Generative.openai(
            # Name of the OpenAI model to use for generation
                model="gpt-4o"
            )
        )
        # Print a message to indicate that the collection was created
        print("Collection created successfully!")
    else:
        # Print a message to indicate that the collection already exists
        print("Collection already exists!")
# If there is an error, print the error message
except Exception as e:
    print(f"Error creating collection: {e}")

# Request data which will be imported into the collection
resp = requests.get(
    "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
)
# Parse the JSON data
data = json.loads(resp.text)

# Get the collection where the data will be imported
questions = client.collections.get("Question")

# Import the data into the collection as batch objects
with questions.batch.dynamic() as batch:
    # Iterate over the data and add each object to the batch
    for d in data:
        batch.add_object({
            # The "answer" property will be used for semantic search
            "answer": d["Answer"],
            # The "question" property will be used for generation
            "question": d["Question"],
            # The "category" property will be used for filtering
            "category": d["Category"],
        })

# Query the collection for semantic search
query_text = "biology"
# Limit the number of results
limit = 2
# Query the collection
results = questions.query.near_text(
    query=query_text,
    limit=limit
)

# Print the results
print(results)

# RAG technique using Weaviate and OpenAI to generate a response based on the nearest text for the query to accomplish a task
# Query text
query_text = "biology"
# Limit the number of results
limit = 2
# Grouped task
grouped_task = "Write a tweet with emojis about these facts."

# Generate the response
response = questions.generate.near_text(
    query=query_text,
    limit=limit,
    grouped_task=grouped_task
)

# Print the generated response
print(response.generated)

client.close()