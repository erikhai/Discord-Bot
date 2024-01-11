import discord
import requests
import json
import asyncio  # Import asyncio module for the sleep function




def get_random_media(media_type):
    # Define the API endpoints for memes, manga, anime and news
    api_endpoints = {
        'meme': 'https://meme-api.com/gimme',
        'manga': 'https://api.jikan.moe/v4/random/manga',
        'anime': 'https://api.jikan.moe/v4/random/anime',
        'news': 'https://api.nytimes.com/svc/topstories/v2/world.json'
       
    }

    response = requests.get(api_endpoints[media_type])
    json_data = response.json()

    #Extracting the relevant data from the json
    if media_type == 'meme':
        return json_data['url']
    elif media_type == 'news':
        articles = json_data.get('Articles', {})
        print(json_data)
        if articles:
            return f"{articles['title']}\n{articles['Abstract']}\n\nCreated: {articles['created_date']}\nPublished: {articles['published_date']}\n{articles['url']}"
        else:
            return "Unable to fetch article."
    elif media_type == 'manga':
        manga_data = json_data.get('data', {})
        if manga_data:
            genre_names = [genre['name'] for genre in manga_data['genres']]
            return f"Title In Jap: {manga_data['title_japanese']}\nTitle In Eng: {manga_data['title_english']}\nAlternate Titles: {manga_data['title']} \nManga Status: {manga_data['status']}\nSynopsis: {manga_data['synopsis']}\nGenres: {', '.join(genre_names)}\nURL: {manga_data['url']}"
        else:
            return "Unable to fetch random manga."
    elif media_type == 'anime':
        anime_data = json_data.get('data', {})
        if anime_data:
            genre_names = [genre['name'] for genre in anime_data['genres']]
            return f"Title In Jap: {anime_data['title_japanese']}\nTitle In Eng: {anime_data['title_english']}\nAlternate Titles: {anime_data['title']} \nAnime Status: {anime_data['status']}\nSynopsis: {anime_data['synopsis']}\nGenres: {', '.join(genre_names)}\nURL: {anime_data['url']}\nEpisodes {anime_data['episodes']}"
        else:
            return "Unable to fetch random anime."
    else:
        return "Unable to fetch meme."

class MyClient(discord.Client):

    async def on_message(self, message): #async is a keyword that is used to define asynchronous functions. When you declare a function with the async keyword, it becomes an asynchronous function, and you can use the await keyword inside it to wait for the result of another asynchronous function without blocking the execution of the entire program. 
                                         #This allows other tasks to continue while waiting for potentially time-consuming operations to complete. - ChatGPT
        if message.author == self.user: #Ensuring bot does not respond to its own messages
            return
        if message.content.startswith('$@'):
            if message.content.startswith('$@help'):
                await message.channel.send('''Hello coder, these are the commands you can use:
1. $@RandomMeme --> Shows you a meme
2. $@AIChat --> Allows you to chat with the bot (Feature not available yet)
3. $@RandomQuote --> Shares a meaningful quote
4. $@RandomManga --> Shows you a random manga
5. $@RandomAnime --> Shows you a random anime
6. $@RandomJoke --> Shows you a random joke
7. $@WorldNews --> Shows you a top article regarding the world news (Feature not available yet)''')
            elif message.content.startswith('$@RandomMeme'):
                await message.channel.send('Hello coder, here is a meme for you!!')
                await message.channel.send(get_random_media('meme'))
            elif message.content.startswith('$@AIChat'):
                await message.channel.send('Hello coder, this feature is under construction!!')
            
            elif message.content.startswith('$@RandomManga'):
                await message.channel.send('Hello coder, here is a manga for you!!')
                await message.channel.send(get_random_media('manga'))
            elif message.content.startswith('$@RandomAnime'):
                await message.channel.send('Hello coder, here is an anime for you!!')
                await message.channel.send(get_random_media('anime'))
            elif message.content.startswith('$@WorldNews'):
                await message.channel.send('Hello coder, this feature is under construction!!')
                #await message.channel.send('Hello coder, here is an article for you!!')
                #await message.channel.send(get_random_media('news'))
            elif message.content.startswith('$@RandomJoke'):
                await message.channel.send('Hello coder, here is a joke for you!!')
                 
                response = requests.get('https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=twopart')
                json_data = response.json()
              
                if json_data:
                    setup = json_data['setup']
                    delivery = json_data['delivery']

                    # Send setup first
                    await message.channel.send(f"{setup}")

                    # Wait for 2 seconds
                    await asyncio.sleep(2)

                    # Send delivery after 5 seconds
                    await message.channel.send(f"{delivery}")
                else:
                    await message.channel.send("Seems like I cannot make a joke right now due to technical difficulties.")

            elif message.content.startswith('$@RandomQuote'):
                await message.channel.send('Hello coder, here is a quote for you!!')
                response = requests.get('https://api.quotable.io/random')
                quote_data = response.json()

                # Extract the quote and author from the API response
                quote = quote_data['content']
                author = quote_data['author']

                # Send the quote to the Discord channel
                await message.channel.send(f'Here is a meaningful quote written by {author}:\n"{quote}"')

            else:
                await message.channel.send('Sorry coder, you wrote an invalid command for me to interpret. :(')

# Create a Discord Intents object to specify the bot's behavior
intents = discord.Intents.default()

# Enable the tracking of message content to receive message events
intents.message_content = True

# Create an instance of the MyClient class with the specified Intents
client = MyClient(intents=intents)

# Run the Discord bot by connecting to the Discord API with the provided token
client.run('Enter your token')  # Replace with your own token.

