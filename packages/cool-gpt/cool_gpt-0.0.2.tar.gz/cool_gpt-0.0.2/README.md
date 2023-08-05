# cool_gpt

Cool-GPT is a Python library that allows you to use ChatGPT for free using the Selenium framework. 
By utilizing Selenium, you can automate use chatgpt like api, this helps you to generate text and engage in conversations programmatically.
It doesn't require any API keys and it's easy to use and straightforward.
It also doesn't scrape openai or chatgpt website.

## Prerequisites

Before using Cool-GPT, ensure that you have the following prerequisites installed:

- Python 3.6 or above
- Selenium (install via `pip install selenium`)
- element-manager (install via `pip install element-manager`)
- A compatible web driver for Selenium (e.g., ChromeDriver)  [Link](https://chromedriver.chromium.org/downloads)
- Put the web driver in the same folder as the script
- A stable internet connection


## Installation

You can install cool_gpt via pip:

```bash
pip install cool_gpt
```

## Getting Started

To get started, follow these steps:

### [Basic Usage] Here's a basic example of how to use cool_gpt:

Install: `pip install cool-gpt==0.0.1` or `pip install cool-gpt`

**NOTE: cool-gpt==0.0.1 doesn't support text to speech and speech to text**


```
from cool_gpt import bot

driver = bot.setup_driver()
print('Enter 'q' to quit')
while True:
    message = input('You: ')
    if message == 'q':
        break
    print('Bot:', bot.ask(message, driver))
```

### [Advance Usage] It also supports text to speech and speech to text:

Install: `pip install cool-gpt`

```
from cool_gpt import bot
from cool_gpt.speech_to_text.speech_to_text import speech_to_text_google
from cool_gpt.speech_to_text.speech_to_text_whisper import speech_to_text_whisper
from cool_gpt.text_to_speech.text_to_speech import text_to_speech

driver = bot.setup_driver(debug=False)
while True:
    # message = input('You: ') # for text input
    message, status = speech_to_text_whisper()  # for speech input via whisper
    # message, status = speech_to_text_google()  # for speech input via gtts
    if status:
        print('You:', message)
        ans = bot.ask(message, driver)
        print('Bot:', ans)
        text_to_speech(ans, backend_tts_api='pyttsx3')  # for speech output via pyttsx3 its free and unlimited
        # _ = text_to_speech(ans, backend_tts_api='gtts')  # for speech output via gtts its free but limited in a day
    else:
        print('Speak again louder please.')
```


## Limitations

Please note the following limitations of cool_gpt:

cool_gpt is dependent on the availability and reliability of the toolbot.ai interface.

Usage of cool_gpt may be subject to the terms and conditions of the service providing the toolbot.ai interface.

Selenium automation may be slower compared to the OpenAI API, and rate limits may apply depending on the provider and toolbot.ai interface.


## Contributing

Contributions to cool_gpt are welcome! If you have any ideas, improvements, or bug fixes, please submit a pull request or open an issue on the GitHub repository.

## License

cool_gpt is licensed under the MIT License. Feel free to use and modify the library according to your needs.

## Acknowledgements

cool_gpt was inspired by the amazing work done by toolbot.ai in developing this amazing website.


## Thank me on-

 - Follow me on Instagram:  [https://www.instagram.com/dipesh_pal17](https://www.instagram.com/dipesh_pal17/)    
        
- Subscribe me on YouTube:  [https://www.youtube.com/dipeshpal17](https://www.youtube.com/dipeshpal17)    