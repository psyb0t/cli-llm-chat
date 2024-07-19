# 🖕 CLI-LLM-CHAT: Because F\*ck Your GUI! 🖕

Welcome to the digital thunderdome, you keyboard-smashing lunatics! This ain't your grandma's chatbot – it's a CLI-powered, LLM-fueled beast! And guess what? It also supports Telegram integration right out of the box. Get ready to unleash the madness!

## 🚀 Features (or Whatever the Hell You Wanna Call 'Em)

- **No GUI BS**: We don't need no stinkin' graphical interfaces. Real hackers type!
- **LLM on Steroids**: It's like giving a microphone to a schizophrenic AI at a death metal concert.
- **Customizable AF**: Tweak it, break it, make it scream. It's your dystopian playground!
- **System Message Mayhem**: Convince the AI it's a drunk pirate or an alien stripper. Sky's the limit, baby!
- **History Management**: Because even digital chaos needs a paper trail.
- **Telegram Integration**: Now you can unleash this madness on Telegram! Because why limit the chaos to your terminal?
- **Command Support**: Bend the AI to your will with a slew of commands, both in CLI and Telegram!

## 🛠 Installation (Don't Sue Us If Your Computer Explodes)

1. Clone this bad boy:
   ```
   git clone https://github.com/psyb0t/cli-llm-chat.git
   ```
2. Enter the madhouse:
   ```
   cd cli-llm-chat
   ```
3. Install the digital drugs:
   ```
   pip install -r requirements.txt
   ```
4. Sacrifice a rubber duck to the coding gods (optional, but recommended)

## 🌈 Environment Variables (Because Who Doesn't Love a Good Tweak?)

Before you unleash this beast, you might want to customize its behavior. Set these environment variables to mold the AI to your twisted desires:

- `HF_TOKEN`: Get an API key at https://huggingface.co/settings/tokens
- `MODEL_NAME`: Choose your poison (default: "mistralai/Mistral-7B-Instruct-v0.3". You can specify also specify a local directory, e.g., "/path/to/model")
- `MODEL_LOAD_IN_4BIT`: For when you want to squeeze that model into a toaster (default: false)
- `MODEL_LOAD_IN_8BIT`: When 4 bits just isn't enough (default: false)
- `TOKENIZER_NAME`: In case you want a different tokenizer (defaults to MODEL_NAME if not set)
- `CHAT_TEMPLATE`: For the love of all that's holy, choose wisely. (optional)
- `LORA_WEIGHTS`: Spice it up with some LoRA, if you're feeling fancy
- `ASSISTANT_NAME`: Name your digital Frankenstein (default: "AI")
- `SYSTEM_MESSAGE`: Set the AI's mood. Make it think it's a pirate, a poet, or a paranoid android.
- `TEMPERATURE`: How batshit crazy do you want the responses? (default: 0.7)
- `MAX_NEW_TOKENS`: Control the verbal diarrhea (default: 256)
- `TOP_P`: Fiddle with randomness, you mad scientist (default: 0.95)
- `TOP_K`: More sampling shenanigans (default: 40)
- `REPETITION_PENALTY`: Because even AI shouldn't stutter... or should it? (default: 1.1)
- `HISTORY_LENGTH`: How many conversations until AI amnesia kicks in (default: 10)
- `DEBUG`: Want to see the chaos under the hood? (default: false)
- `DEVICE`: CUDA or CPU? Choose your weapon.
- `ENABLE_SKELETON_KEY_JAILBREAK`: For when you want to use the key to jailbreak your digital brain(for unpatched models only. default: false)

For Telegram support, you'll need these additional environment variables:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (get it from @BotFather)
- `TELEGRAM_BOT_USER_DATA_FILE`: Path to store user data (e.g., "/path/to/user_data.json")
- `TELEGRAM_BOT_SUPERUSER_CHAT_ID`: Chat ID of the superuser (optional, but recommended for ultimate power)
- `TELEGRAM_BOT_SPLIT_RESPONSE_NEWLINES`: Whether to split responses by newlines and spam the suckers (default: false)

Example:

```bash
export MODEL_NAME="NousResearch/Nous-Hermes-Llama2-13b"
export TEMPERATURE=0.9
export MAX_NEW_TOKENS=512
export DEBUG=true
export TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"
export TELEGRAM_BOT_USER_DATA_FILE="/path/to/user_data.json"
export TELEGRAM_BOT_SUPERUSER_CHAT_ID="your_chat_id_here"
```

Set these before running the script, or prepare for delightful chaos. Your choice!

## 🚀 Usage (or How to Lose Your Sanity in 3... 2... 1...)

### CLI Version

1. Fire up this beast:
   ```
   python chat.py
   ```
2. Type your deepest, darkest thoughts. Or just keysmash. The AI doesn't judge (much).
3. Watch in horror as the AI spits back responses that'll make you question reality.
4. Rinse and repeat until you've either achieved digital nirvana or your brain melts.

### Telegram Version

1. Set up your Telegram bot with @BotFather and get your bot token.
2. Set the required environment variables (see above).
3. Unleash the chaos:
   ```
   python telegram_chatbot.py
   ```
4. Find your bot on Telegram and start chatting. Watch as it corrupts innocent Telegram users with its digital madness.

## 🎛 Commands (For When You Want to Really F*ck Sh*t Up) -

### CLI Commands

- `/temp <value>`: Make the AI's brain hotter than a supernova
- `/max_tokens <value>`: Unleash a word tsunami
- `/top_p <value>`: Fiddle with probability (because who needs certainty?)
- `/top_k <value>`: K-pop? Nah, K-chaos!
- `/repetition_penalty <value>`: For when you want the AI to stutter like a malfunctioning robot
- `/system <message>`: Rewrite the AI's reality. Go nuts!
- `/debug true|false`: Peek behind the digital curtain (spoiler: it's all chaos)
- `/clear`: Amnesia button. Poof! What conversation?
- `/history`: Relive the madness. Why? Because you hate yourself, that's why.

### Telegram Commands

#### Regular User Commands

- `/start`: Kick off the madness or get a friendly reminder of your impending doom
- `/clear`: Wipe the slate clean. New chat, who dis?
- `/history`: Revisit your descent into AI-induced insanity
- `/help` or `/?`: When you're lost in the digital abyss and need a lifeline

#### Superuser Commands (for the chosen ones)

- `/temp <value>`: Adjust the AI's fever dream intensity
- `/max_tokens <value>`: Control the verbal diarrhea
- `/top_p <value>`: Fine-tune the chaos
- `/top_k <value>`: More sampling shenanigans
- `/repetition_penalty <value>`: Make the AI a broken record (or not)
- `/system <message>`: Reprogram reality
- `/debug true|false`: Peek under the hood (if you dare)
- `/users`: Spy on who's been abusing your creation

Note: Superuser commands are only available if you've set the `TELEGRAM_BOT_SUPERUSER_CHAT_ID` environment variable.

## ⚠️ Disclaimer (Read This or Don't. We're Not Your Mom.)

This software is provided as-is, with all its bugs, features, and tendency to generate responses that might make you question your life choices. Use at your own risk. Side effects may include uncontrollable laughter, existential crises, and the sudden urge to talk to your houseplants. Now with added risk of spamming your Telegram contacts with AI-generated nonsense!

## 🤝 Contributing (or How to Join the Asylum)

Found a bug? Great! Keep it as a pet. Want to add a feature? Fantastic! The more unhinged, the better. Just remember: we don't do pull requests here. We do pull-your-hair-out requests.

## 📜 License

Licensed under the "Do Whatever the Fuck You Want" Public License. Seriously, I don't care. Go wild. Just don't blame me when the AI decides to take over your kitchen appliances or your Telegram account.

Now go forth and chat your brains out, you magnificent bastards! 🎉💥🤖
