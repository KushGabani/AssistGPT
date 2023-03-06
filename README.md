<h1 align="center">

AssistGPT

</h1>

---

## 🚀 Set up the project on a local machine
1. Clone the repository to your desired location
    ```shell
    git clone https://github.com/KushGabani/AssistGPT
    ```
2. Login/Signup into your OpenAI account and get your API key from Account > [API Keys](https://openai.com/api/).
3. Use our Telegram Bot @AssistGPT or create your own Telegram bot token from [@BotFather](https://t.me/BotFather)
4. Create a `.env` file and copy the contents of the `.env.sample` and add your tokens there
5. Create a virtual environment using virtualenv or conda.
```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate

# or using Conda
conda create -n chatbot python==3.10.8
conda activate chatbot
```
6. Install python dependencies for the project
```shell
pip install -r requirements.txt
```
7. Change working directory
```shell
cd AssistGPT
```
9. Run the bot using
```shell
python bot/bot.py
```