<h1 align="center">🤖 Feedback Bot</h1>

#### This is a feedback bot.

Bot example: [@NessFeedbackBot](https://NessFeedbackBot.t.me)

## Features

* Separate topics in the group for each user.
* Lock user on topic close and unlock on resume.
* Localization in two languages (russian and english)

## Known Bugs

* When closing and after deleting a topic, user messages are not sent to the feedback chat.

## Requirements

* Python 3.10 and above.
* Systemd or Docker.

## Usage

Clone this repo via [link](https://github.com/nessshon/feedback-bot)

```bash
git clone https://github.com/nessshon/feedback-bot
```

Go to the project folder

```bash
cd feedback-bot
```

Create environment variables file

```bash
cp .env.example .env
```

Edit [environment variables](#environment-variables-reference) in `.env`

```bash
nano .env
```

### Launch using Docker

1. Install [docker](https://docs.docker.com/get-docker) and [docker compose](https://docs.docker.com/compose/install/)

2. Build and run your container
   ```bash
   docker-compose up -d
   ```

### Launch using systemd

1. Create a virtual environment
   ```bash
   python3.10 -m venv env
   ```

2. Activate virtual environment
   ```bash
   source env/bin/activate
   ```

3. Install required packages
   ```bash
   pip install -r requirements.txt
   ```

4. Check if the bot is running
   ```bash
   python -m app
   ```

5. Set **WorkingDirectory** to the path to the project folder.
   ```bash
   nano telegram-bot.service
   ```

6. Copy telegram-bot.service to /lib/systemd/system/
   ```bash
   sudo cp telegram-bot.service /lib/systemd/system/feedback-bot.service
   ```
7. Enable autostart on boot
   ```bash
   sudo systemctl enable feedback-bot.service
   ```
8. Launch Bot
   ```bash
   sudo systemctl start feedback-bot.service
   ```

### Environment variables reference

| Variable        | Description                                                                                                                  |
|-----------------|------------------------------------------------------------------------------------------------------------------------------|
| BOT_TOKEN       | Token, get it from [@BotFather](https://t.me/BotFather)                                                                      |
| GROUP_CHAT_ID   | Group ID where messages from users will be sent. Don't forget to enable themes in the group and add admin rights to the bot. |
| CUSTOM_EMOJI_ID | Emoji custom ID, recommended 5417915203100613993                                                                             |
