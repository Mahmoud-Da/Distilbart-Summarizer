# Model and summarization defaults
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
DEFAULT_MIN_LENGTH = 30
DEFAULT_MAX_LENGTH = 150
# Percentage of model's max length to use for chunks
# We use a chunk size slightly smaller than the max length to leave room for summarization tokens
# A 75% factor is a safe bet.
CHUNK_SIZE_FACTOR = 0.75

# Device configuration
USE_CUDA_IF_AVAILABLE = True
