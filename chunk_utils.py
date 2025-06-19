from typing import List

from transformers import AutoTokenizer


def chunk_text(text: str, tokenizer: AutoTokenizer, chunk_size: int) -> List[str]:
    tokens = tokenizer.encode(text)
    token_chunks = [tokens[i:i + chunk_size]
                    for i in range(0, len(tokens), chunk_size)]
    return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in token_chunks]
