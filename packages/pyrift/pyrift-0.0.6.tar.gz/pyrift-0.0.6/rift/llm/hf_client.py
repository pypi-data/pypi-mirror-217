import asyncio
from pydantic import BaseSettings, BaseModel
from rift.llm.abstract import AbstractCodeCompletionProvider, InsertCodeResult

from rift.util.TextStream import TextStream
from .openai_types import (
    Message,
)
from typing import Any, Optional
import time
import datetime
import json
import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging

logger = logging.getLogger(__name__)

_mock_string = """```
def mock():
    endpoint = "/chat/completions"
    input_type = ChatCompletionRequest
    params = ChatCompletionRequest(messages=messages, stream=stream, **kwargs)
    output_type = ChatCompletionResponse

    if stream:
        return self._post_streaming(
            endpoint,
            params=params,
            input_type=input_type,
            stream_data_type=ChatCompletionChunk,
        )
    else:
        return self._post_endpoint(
            endpoint, params=params, input_type=input_type, output_type=output_type
        )
```
"""


class DataOutput(BaseModel):
    id: str
    created: str
    text: str


PastKv = tuple[tuple[torch.Tensor, ...], ...]


class HuggingFaceClient(AbstractCodeCompletionProvider):
    temperature: int = 1
    max_len: int = 128  # todo: short length for testing purpose. Maybe need to make it to 2048 in production?

    def __init__(self, model_name = None):
        model_name = model_name or "Salesforce/codegen-350m-mono"
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def infer(self, kwargs):
        return self.model(**kwargs)

    async def _insert_code_core(self, document: str, cursor_offset: int):
        code = document

        prompt_tokens = self.tokenizer(code, return_tensors="pt")
        buffer = []
        generated = ""
        past_kv: Optional[PastKv] = None

        while True:
            kwargs: dict
            if past_kv is None:
                kwargs = prompt_tokens  # type: ignore
            else:
                kwargs = dict(
                    input_ids=buffer[-1][:, None],
                    attention_mask=torch.ones_like(buffer[-1][:, None]),
                )
            kwargs["use_cache"] = True
            kwargs["past_key_values"] = past_kv
            model_output = await asyncio.get_event_loop().run_in_executor(
                None, self.infer, kwargs
            )

            outputs: torch.Tensor = model_output.logits
            past_kv = model_output.past_key_values
            logits = outputs[:, -1] * 1.0 / self.temperature
            out_tk = logits.argmax(-1)
            buffer.append(out_tk)
            # todo: may need a better stopping criteria such as when it completes a function (no indent)
            if (
                out_tk.squeeze().item() == 50256
                or len(buffer) + len(prompt_tokens) >= self.max_len
            ):
                break

            # can modify the behavior here into line-by-line yield
            new_word = self.tokenizer.decode(out_tk.squeeze())

            if "\n" in new_word:
                result = generated.split("\n")[-1] + new_word.split("\n")[0]
                yield result
                for line in new_word.split("\n")[1:]:
                    yield line + "\n"
            generated += new_word

    async def insert_code(self, document: str, cursor_offset: int, goal=None):
        if goal is not None:
            logger.warn(
                "goal parameter is not supported yet for huggingface models. Ignoring."
            )
        code = TextStream.from_aiter(self._insert_code_core(document, cursor_offset))
        return InsertCodeResult(code=code)
