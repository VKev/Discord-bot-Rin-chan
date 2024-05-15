# Discord-bot-Rin

A discord bot that can sing, generate image, ask gpt

## Docker:

```console
docker pull vkev25811/rinchandiscordbot:v1.0
```

Remember to add DISCORD_BOT_KEY env variable and set it to your discord bot token when run image

## Command:

**!help** : display tutorial and list of commands

**!clear** [*_Amount_*] : Clear amount of messages, max 50

**!ping** : display bot ping

**!p** [*_Name of song or youtube url_*] : play the song, add to queue

**!vol** [*_Volume_*] : Set song volume

**!dc** : Disconnect bot from current voice channel

**!skip**: skip the song

**!queue** : view song queue

**!gpt3** [*_Question_*] : ask chatgpt 3.5 question, fast response time

**!gpt4** [*_Question_*] : ask chatgpt 4.0 question, slowly but surely

**!dall3** [*_Image description_*] : generate image base on image description

# Enter your bot token in rin.py to use

<img src="/ShowCase/gpt3.png" style="margin-top: 30px;" alt="showing"/>
    
    Model: gpt-3.5-turbo

<img src="/ShowCase/dall3.png" style="margin-top: 30px;" alt="showing"/>
    
    Model: dall-e-3

<img src="/ShowCase/music.png" style="margin-top: 30px;" alt="showing"/>
