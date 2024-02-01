import torch
import os
from transformers import (
    AutoModelForCausalLM,
    pipeline,
    AutoTokenizer,
    TextIteratorStreamer,
)
from threading import Thread


DEVICE = "cuda"
MODEL_NAME = os.getenv(
    "MODEL_NAME", "TheBloke/SOLAR-10.7B-Instruct-v1.0-uncensored-GPTQ"
)

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "AI")
SYSTEM_MESSAGE = os.getenv("SYSTEM_MESSAGE", "You are a helpful AI assistant")

TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 256))

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(DEVICE)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    device=DEVICE,
)


def get_chat_ml_conversation(user, assistant="", system=None):
    conversation = ""
    if system:
        conversation += f"<|system|>\n{system}</s>\n"

    conversation += f"<|user|>\n{user}</s>\n<|assistant|>\n{assistant}"

    return conversation


def get_prompt(user):
    return get_chat_ml_conversation(
        user=user,
        assistant="",
        system="you are a helpful AI assistant",
    )


def cmd_set_temperature(temp):
    global TEMPERATURE
    TEMPERATURE = temp


def cmd_set_max_new_tokens(num):
    global MAX_NEW_TOKENS
    MAX_NEW_TOKENS = num


# Function to process input and generate response
def generate_response(input_text):
    inputs = tokenizer(
        [get_prompt(input_text)],
        return_tensors="pt",
    )

    inputs["input_ids"] = inputs["input_ids"].to("cuda")
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True)

    generation_kwargs = dict(
        inputs,
        streamer=streamer,
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=True,
        temperature=TEMPERATURE,
        top_p=0.95,
        top_k=40,
        repetition_penalty=1.1,
    )

    Thread(target=model.generate, kwargs=generation_kwargs).start()

    print(f"\n{ASSISTANT_NAME}: ", end="")

    assistent_text = ""
    for assistent_text_part in streamer:
        print(assistent_text_part, end="")

        assistent_text += assistent_text_part

    print("\n" * 2)


def cmd_get_prompt():
    return get_prompt("example user input")


def exec_command(user_input):
    cmd_args = user_input.split("(")
    cmd = cmd_args[0]
    args = ""

    if len(cmd_args) > 1:
        args = cmd_args[1]

    args = args.strip(")").split(",")

    if cmd == "get_prompt":
        print(cmd_get_prompt())
    elif cmd == "set_temperature":
        if len(args) < 1:
            print("USAGE: set_temperature(temperature)")

        cmd_set_temperature(float(args[0]))

    elif cmd == "set_max_new_tokens":
        if len(args) < 1:
            print("USAGE: set_max_new_tokens(max_new_tokens)")

        cmd_set_max_new_tokens(int(args[0]))

    elif cmd == "get_commands" or cmd == "help" or cmd == "commands" or cmd == "?":
        print("get_prompt")
        print("set_temperature(temperature)")
        print("set_max_new_tokens(max_new_tokens)")
    else:
        generate_response(user_input)


while True:
    user_input = input("You: ")
    if user_input == "":
        break

    exec_command(user_input)
