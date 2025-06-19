import torch
from tqdm import tqdm
from transformers import AutoTokenizer, pipeline

from config import (CHUNK_SIZE_FACTOR, DEFAULT_MAX_LENGTH, DEFAULT_MIN_LENGTH,
                    MODEL_NAME, USE_CUDA_IF_AVAILABLE)

from chunk_utils import chunk_text


class LongTextSummarizer:
    def __init__(self, model_name=MODEL_NAME):
        self.device = "cuda" if USE_CUDA_IF_AVAILABLE and torch.cuda.is_available() else "cpu"
        # device=0 maps to the first GPU, device=-1 maps to the CPU.
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            device=0 if self.device == "cuda" else -1,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model_max_length = self.summarizer.model.config.max_position_embeddings

    def summarize(self, text: str, min_length=DEFAULT_MIN_LENGTH, max_length=DEFAULT_MAX_LENGTH) -> str:
        num_tokens = len(self.tokenizer.encode(text))

        if num_tokens < self.model_max_length:
            return self._summarize_chunk(text, min_length, max_length)

        chunks = chunk_text(text, self.tokenizer, int(
            self.model_max_length * CHUNK_SIZE_FACTOR))
        chunk_summaries = [
            self._summarize_chunk(
                chunk,
                max(20, int(len(self.tokenizer.encode(chunk)) * 0.5)),
                int(len(self.tokenizer.encode(chunk)) * 0.5)
            )
            for chunk in tqdm(chunks, desc="Summarizing Chunks")
        ]

        return self.summarize(" ".join(chunk_summaries), min_length, max_length)

    def _summarize_chunk(self, chunk: str, min_len: int, max_len: int) -> str:
        return self.summarizer(
            chunk,
            min_length=min_len,
            max_length=max_len,
            do_sample=False
        )[0]['summary_text']
