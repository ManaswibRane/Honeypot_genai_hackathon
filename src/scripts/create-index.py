from google.cloud import aiplatform

PROJECT_ID = "your-project-id"
REGION = "us-central1"

aiplatform.init(project=PROJECT_ID, location=REGION)

index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name="threat-intel-index",
    dimensions=768,  # REQUIRED for text-embedding-004
    approximate_neighbors_count=150,
)

print("INDEX_ID =", index.resource_name)
