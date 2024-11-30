import weaviate

# Connect to local Weaviate instance running in Docker Compose
client = weaviate.connect_to_local(
    port=32360,
    grpc_port=30984
)

try:    
    client.collections.delete("Question")
except Exception as e:
    print(f"Error deleting collection: {e}")

# Close the client
client.close()