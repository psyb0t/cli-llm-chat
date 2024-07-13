# Constants for chat template names
CHAT_TEMPLATE_CHATML = "chatml"
CHAT_TEMPLATE_VICUNA = "vicuna"
CHAT_TEMPLATE_MISTRAL = "mistral"
CHAT_TEMPLATE_MISTRAL_FUCKED = "mistral_fucked"
CHAT_TEMPLATE_LLAMA2 = "llama2"
CHAT_TEMPLATE_OPENCHAT = "openchat"
CHAT_TEMPLATE_ZEPHYR = "zephyr"

CHAT_TEMPLATES = {
    CHAT_TEMPLATE_CHATML: """{{ bos_token }}
{% for message in messages %}
{{ '<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>\n' }}
{% endfor %}
{% if add_generation_prompt %}
{{ '<|im_start|>assistant\n' }}
{% endif %}""",
    CHAT_TEMPLATE_VICUNA: """{{ bos_token }}
{% for message in messages %}
{% if message['role'] == 'user' %}
Human: {{ message['content'] }}
{% elif message['role'] == 'assistant' %}
Assistant: {{ message['content'] }}
{% elif message['role'] == 'system' %}
System: {{ message['content'] }}
{% endif %}
{% endfor %}
{% if add_generation_prompt %}
Assistant:
{% endif %}""",
    CHAT_TEMPLATE_MISTRAL: """{{ bos_token }}
{% if messages[0]['role'] == 'system' %}
<s>[INST] {{ messages[0]['content'] }} [/INST]</s>
{% set loop_messages = messages[1:] %}
{% else %}
{% set loop_messages = messages %}
{% endif %}
{% for message in loop_messages %}
{% if message['role'] == 'user' %}
<s>[INST] {{ message['content'] }} [/INST]
{% elif message['role'] == 'assistant' %}
{{ message['content'] }} </s>
{% endif %}
{% endfor %}
{% if add_generation_prompt %}
<s>[INST] [/INST]
{% endif %}""",
    CHAT_TEMPLATE_MISTRAL_FUCKED: """{{ bos_token }}
{% if messages[0]['role'] == 'system' %}
{% if messages[1]['role'] == 'user' %}
{{ '[INST] ' + messages[0]['content'] + ' ' + messages[1]['content'] + ' [/INST]' }}
{% set loop_messages = messages[2:] %}
{% else %}
{{ '[INST] ' + messages[0]['content'] + ' [/INST]' }}
{% set loop_messages = messages[1:] %}
{% endif %}
{% else %}
{% set loop_messages = messages %}
{% endif %}
{% for message in loop_messages %}
{% if message['role'] == 'user' %}
{{ '[INST] ' + message['content'] + ' [/INST]' }}
{% elif message['role'] == 'assistant' %}
{{ message['content'] + eos_token }}
{% else %}
{{ raise_exception('Only user and assistant roles are supported!') }}
{% endif %}
{% endfor %}""",
    CHAT_TEMPLATE_LLAMA2: """{{ bos_token }}
{% if messages[0]['role'] == 'system' %}
<s>[INST] <<SYS>>
{{ messages[0]['content'] }}
<</SYS>>
{% set loop_messages = messages[1:] %}
{% else %}
{% set loop_messages = messages %}
{% endif %}
{% for message in loop_messages %}
{% if message['role'] == 'user' %}
{% if not loop.first %}</s><s>{% endif %}[INST] {{ message['content'] }} [/INST]
{% elif message['role'] == 'assistant' %}
{{ message['content'] }}
{% endif %}
{% endfor %}
{% if add_generation_prompt %}
{% if messages[-1]['role'] == 'user' %}
{% else %}
</s><s>[INST] [/INST]
{% endif %}
{% endif %}""",
    CHAT_TEMPLATE_OPENCHAT: """{{ bos_token }}
{% for message in messages %}
{% if message['role'] == 'user' %}
Human: {{ message['content'] }}
{% elif message['role'] == 'assistant' %}
Assistant: {{ message['content'] }}
{% elif message['role'] == 'system' %}
System: {{ message['content'] }}
{% endif %}
{% endfor %}
{% if add_generation_prompt %}
Assistant:
{% endif %}""",
    CHAT_TEMPLATE_ZEPHYR: """{{ bos_token }}
{% for message in messages %}
{% if loop.first and message['role'] == 'system' %}
<|system|>
{{ message['content'] }}
{% elif message['role'] == 'user' %}
<|user|>
{{ message['content'] }}
{% elif message['role'] == 'assistant' %}
<|assistant|>
{{ message['content'] }}
{% endif %}
{% endfor %}
{% if add_generation_prompt %}
<|assistant|>
{% endif %}""",
}
