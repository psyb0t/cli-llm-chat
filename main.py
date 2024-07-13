import os
from typing import List, Dict, Optional, Union
import torch
import logging
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TextIteratorStreamer,
    BitsAndBytesConfig,
)
from peft import PeftModel
from threading import Thread
from common import CHAT_TEMPLATES

logging.getLogger("transformers").setLevel(logging.ERROR)

# Constants for default values
DEFAULT_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
DEFAULT_ASSISTANT_NAME = "AI"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_NEW_TOKENS = 256
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_K = 40
DEFAULT_REPETITION_PENALTY = 1.1
DEFAULT_HISTORY_LENGTH = 10

# Constants for environment variable names
ENV_VAR_MODEL_NAME = "MODEL_NAME"
ENV_VAR_ASSISTANT_NAME = "ASSISTANT_NAME"
ENV_VAR_SYSTEM_MESSAGE = "SYSTEM_MESSAGE"
ENV_VAR_TEMPERATURE = "TEMPERATURE"
ENV_VAR_CHAT_TEMPLATE = "CHAT_TEMPLATE"
ENV_VAR_MAX_NEW_TOKENS = "MAX_NEW_TOKENS"
ENV_VAR_TOP_P = "TOP_P"
ENV_VAR_TOP_K = "TOP_K"
ENV_VAR_REPETITION_PENALTY = "REPETITION_PENALTY"
ENV_VAR_HISTORY_LENGTH = "HISTORY_LENGTH"
ENV_VAR_DEBUG = "DEBUG"
ENV_VAR_DEVICE = "DEVICE"
ENV_VAR_MODEL_LOAD_IN_4BIT = "MODEL_LOAD_IN_4BIT"
ENV_VAR_MODEL_LOAD_IN_8BIT = "MODEL_LOAD_IN_8BIT"
ENV_VAR_TOKENIZER_NAME = "TOKENIZER_NAME"
ENV_VAR_LORA_WEIGHTS = "LORA_WEIGHTS"
ENV_VAR_HF_TOKEN = "HF_TOKEN"


class Chatbot:
    def __init__(self) -> None:
        self.huggingface_token: str = os.getenv(ENV_VAR_HF_TOKEN, "")

        model_name: str = os.getenv(ENV_VAR_MODEL_NAME, "")
        self.model_name: str = model_name if model_name else DEFAULT_MODEL_NAME

        tokenizer_name: str = os.getenv(ENV_VAR_TOKENIZER_NAME, "")
        self.tokenizer_name: str = tokenizer_name if tokenizer_name else self.model_name

        self.chat_template: str = os.getenv(ENV_VAR_CHAT_TEMPLATE, "")

        assistant_name: str = os.getenv(ENV_VAR_ASSISTANT_NAME, "")
        self.assistant_name: str = (
            assistant_name if assistant_name else DEFAULT_ASSISTANT_NAME
        )

        self.system_message: str = os.getenv(ENV_VAR_SYSTEM_MESSAGE, "")

        self.temperature: float = float(
            os.getenv(ENV_VAR_TEMPERATURE, DEFAULT_TEMPERATURE)
        )

        self.max_new_tokens: int = int(
            os.getenv(ENV_VAR_MAX_NEW_TOKENS, DEFAULT_MAX_NEW_TOKENS)
        )

        self.top_p: float = float(os.getenv(ENV_VAR_TOP_P, DEFAULT_TOP_P))
        self.top_k: int = int(os.getenv(ENV_VAR_TOP_K, DEFAULT_TOP_K))

        self.repetition_penalty: float = float(
            os.getenv(ENV_VAR_REPETITION_PENALTY, DEFAULT_REPETITION_PENALTY)
        )

        self.history: List[Dict[str, str]] = []
        self.history_length: int = int(
            os.getenv(ENV_VAR_HISTORY_LENGTH, DEFAULT_HISTORY_LENGTH)
        )

        self.debug: bool = os.getenv(ENV_VAR_DEBUG, "false").lower() == "true"

        self.device: str = os.getenv(
            ENV_VAR_DEVICE, "cuda" if torch.cuda.is_available() else "cpu"
        )

        self.load_in_4bit = (
            os.getenv(ENV_VAR_MODEL_LOAD_IN_4BIT, "false").lower() == "true"
        )

        self.load_in_8bit = (
            os.getenv(ENV_VAR_MODEL_LOAD_IN_8BIT, "false").lower() == "true"
        )

        self.lora_weights: str = os.getenv(ENV_VAR_LORA_WEIGHTS, "")

        if self.debug:
            self.print_debug_info()

        quantization_config = None
        if self.load_in_4bit:
            print("Loading in 4-bit precision")
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16
            )
        elif self.load_in_8bit:
            print("Loading in 8-bit precision")
            quantization_config = BitsAndBytesConfig(load_in_8bit=True)

        print(f"Loading model: {self.model_name}")
        self.model: AutoModelForCausalLM = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map=self.device,
            quantization_config=quantization_config,
            token=self.huggingface_token,
        )

        print(f"Loading tokenizer: {self.tokenizer_name}")
        self.tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(
            self.tokenizer_name,
            use_fast=True,
            token=self.huggingface_token,
        )

        if self.chat_template:
            print(f"Setting chat template to: {self.chat_template}")
            self.tokenizer.chat_template = CHAT_TEMPLATES[self.chat_template]

        if not self.tokenizer.chat_template:
            if self.tokenizer.default_chat_template:
                print(
                    f"Setting chat template to default one: {self.tokenizer.default_chat_template}"
                )
                self.tokenizer.chat_template = self.tokenizer.default_chat_template

        if self.lora_weights:
            print(f"Loading LoRA weights from: {self.lora_weights}")
            self.model = PeftModel.from_pretrained(
                self.model,
                self.lora_weights,
                token=self.huggingface_token,
            )
            print(f"Loaded LoRA weights from {self.lora_weights}")

        print(f"Verifying vocab sizes for model and tokenizer")
        base_vocab_size = self.model.get_input_embeddings().weight.shape[0]
        tokenizer_vocab_size = len(self.tokenizer)
        if base_vocab_size != tokenizer_vocab_size:
            print(
                f"Warning: Mismatch between model vocab size ({base_vocab_size}) "
                f"and tokenizer vocab size ({tokenizer_vocab_size})"
            )

        self.model.config.tokenizer = self.tokenizer

        # Set pad token if not set
        if self.tokenizer.pad_token is None:
            print(f"Setting pad_token to eos_token: {self.tokenizer.eos_token}")
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        # Set the padding side
        self.tokenizer.padding_side = "left"

    def print_debug_info(self):
        print("\n--- Chat Debug Information ---")
        print("Model Name:", self.model_name)
        print("Tokenizer Name:", self.tokenizer_name)
        print("Assistant Name:", self.assistant_name)
        print("System Message:", self.system_message)
        print("Temperature:", self.temperature)
        print("Max New Tokens:", self.max_new_tokens)
        print("Top P:", self.top_p)
        print("Top K:", self.top_k)
        print("Repetition Penalty:", self.repetition_penalty)
        print("History Length:", self.history_length)
        print("Debug:", self.debug)
        print("Device:", self.device)
        print("Load in 4-bit:", self.load_in_4bit)
        print("Load in 8-bit:", self.load_in_8bit)
        print("Lora Weights:", self.lora_weights)
        print("--- End Chat Debug Information ---\n")

    def print_prompt_debug_info(
        self,
        prompt: str,
        generation_kwargs: Dict[
            str, Union[torch.Tensor, TextIteratorStreamer, int, bool, float]
        ],
    ) -> None:
        print("\n--- Debug Information ---")
        print("Prompt:")
        print(prompt)
        print("\nGeneration Parameters:")
        for key, value in generation_kwargs.items():
            if key != "inputs" and key != "streamer":
                print(f"{key}: {value}")
        print("--- End Debug Information ---\n")

    def generate_response(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})
        self.history = self.history[
            -self.history_length :
        ]  # Keep only the last n messages

        messages = self.history
        if self.system_message:
            messages = [{"role": "system", "content": self.system_message}] + messages[
                -self.history_length - 1 :
            ]

        prompt: str = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=False
        )

        inputs: Dict[str, torch.Tensor] = self.tokenizer(
            prompt,
            return_tensors="pt",
            padding=True,
            # truncation=True,
            # max_length=self.tokenizer.model_max_length,
        ).to(self.device)

        streamer: TextIteratorStreamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, skip_special_tokens=True
        )

        generation_kwargs: Dict[
            str, Union[torch.Tensor, TextIteratorStreamer, int, bool, float]
        ] = {
            "inputs": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
            "streamer": streamer,
            "max_new_tokens": self.max_new_tokens,
            "do_sample": True,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repetition_penalty": self.repetition_penalty,
        }

        if self.debug:
            self.print_prompt_debug_info(prompt, generation_kwargs)

        Thread(target=self.model.generate, kwargs=generation_kwargs).start()

        print(f"\n{self.assistant_name}: ", end="", flush=True)
        assistant_response: str = ""
        for text in streamer:
            print(text, end="", flush=True)
            assistant_response += text

        print("\n")
        self.history.append(
            {"role": "assistant", "content": assistant_response.strip()}
        )
        return assistant_response.strip()

    def set_parameter(self, param: str, value: Union[float, int, str]) -> None:
        if param in ["temperature", "top_p", "repetition_penalty"]:
            setattr(self, param, float(value))
        elif param in ["max_new_tokens", "top_k"]:
            setattr(self, param, int(value))
        elif param == "system_message":
            setattr(self, param, str(value))
        elif param == "debug":
            setattr(self, param, value.lower() == "true")
        print(f"{param.capitalize()} set to: {getattr(self, param)}")

    def clear_history(self) -> None:
        self.history.clear()
        print("Chat history cleared")

    def show_history(self) -> None:
        for entry in self.history:
            print(f"{entry['role'].capitalize()}: {entry['content']}")

    def exec_command(self, user_input: str) -> Optional[str]:
        if user_input.startswith("/"):
            cmd_parts: List[str] = user_input[1:].split(None, 1)
            cmd: str = cmd_parts[0]
            args: str = cmd_parts[1] if len(cmd_parts) > 1 else ""

            if cmd in [
                "temp",
                "temperature",
                "max_tokens",
                "top_p",
                "top_k",
                "repetition_penalty",
                "debug",
            ]:
                param = "temperature" if cmd == "temp" else cmd
                param = "max_new_tokens" if param == "max_tokens" else param
                self.set_parameter(param, args)
            elif cmd == "system":
                self.set_parameter("system_message", args)
            elif cmd == "clear":
                self.clear_history()
            elif cmd == "history":
                self.show_history()
            elif cmd in ["help", "?"]:
                print("Available commands:")
                print("/temp <value>: Set temperature")
                print("/max_tokens <value>: Set max new tokens")
                print("/top_p <value>: Set top_p")
                print("/top_k <value>: Set top_k")
                print("/repetition_penalty <value>: Set repetition penalty")
                print("/system <message>: Set system message")
                print("/debug true|false: Enable or disable debug mode")
                print("/clear: Clear chat history")
                print("/history: Show chat history")
                print("/help or /?: Show this help message")
            else:
                print(f"Unknown command: {cmd}")
            return None
        else:
            return self.generate_response(user_input)


def main() -> None:
    chatbot: Chatbot = Chatbot()
    print(f"Chatbot initialized. Type '/help' for available commands.")

    while True:
        user_input: str = input("You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
        if user_input:
            chatbot.exec_command(user_input)


if __name__ == "__main__":
    main()
