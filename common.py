CHAT_TEMPLATES = {
    ## CHATML
    "chatml": """{% for message in messages %}
{{'<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n'}}
{% endfor %}
{% if add_generation_prompt %}
{{ '<|im_start|>assistant\n' }}
{% endif %}""",
    ## VICUNA
    "vicuna": """{% for message in messages %}
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
    ## MISTRAL
    "mistral": """{% if messages[0]['role'] == 'system' %}
<s>[INST] {{ messages[0]['content'] }} [/INST]
</s>
{% endif %}
{% for message in messages %}
{% if message['role'] == 'user' %}
<s>[INST] {{ message['content'] }} [/INST]
{% elif message['role'] == 'assistant' %}
{{ message['content'] }} </s>
{% endif %}
{% endfor %}
{% if add_generation_prompt %}
<s>[INST]  [/INST]
{% endif %}""",
    ## MISTRAL FUCKED
    "mistral_fucked": """{{ bos_token }}{% if messages[0]['role'] == 'system' %}{% if messages[1]['role'] == 'user' %}{{ '[INST] ' + messages[0]['content'] + ' ' + messages[1]['content'] + ' [/INST]' }}{% set loop_messages = messages[2:] %}{% else %}{{ '[INST] ' + messages[0]['content'] + ' [/INST]' }}{% set loop_messages = messages[1:] %}{% endif %}{% else %}{% set loop_messages = messages %}{% endif %}{% for message in loop_messages %}{% if message['role'] == 'user' %}{{ '[INST] ' + message['content'] + ' [/INST]' }}{% elif message['role'] == 'assistant' %}{{ message['content'] + eos_token }}{% else %}{{ raise_exception('Only user and assistant roles are supported!') }}{% endif %}{% endfor %}""",
    ## LLAMA
    "llama2": """{% for message in messages %}
{% if loop.index == 1 and message['role'] == 'system' %}
<s>[INST] <<SYS>>
{{ message['content'] }}
<</SYS>>

{% elif message['role'] == 'user' %}
{{ message['content'] }} [/INST]
{% elif message['role'] == 'assistant' %}
{{ message['content'] }} </s><s>[INST]
{% endif %}
{% endfor %}
{% if add_generation_prompt %}
[/INST]
{% endif %}""",
    ## OPENCHAT
    "openchat": """{% for message in messages %}
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
    ## ZEPHYR
    "zephyr": """{% for message in messages %}
{% if loop.index == 1 and message['role'] == 'system' %}
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
