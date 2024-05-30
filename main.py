import discord
from voice_analysis import get_dbfs

key = 'MTE2NTI1NDMyNzczNzI3NDQwOA.GyzblN.E-iCxZePMTJYQn5Q6jwXE6n8XfSDt6sfSIGrVg'

bot = discord.Bot()
connections = {}


async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    await sink.vc.disconnect()
    for user_id, audio in sink.audio_data.items():
        with open(f"C:/Users/mosina/PycharmProjects/discord-voice-normalization-bot/recordings/{user_id}.mp3",
                  "wb") as f:
            f.write(audio.file.getbuffer())

    # files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    await channel.send(f"Записал голос для: {', '.join(recorded_users)}.")
    list_of_responses, sounds = get_dbfs()
    for i in range(len(list_of_responses)):
        await channel.send(f"Уровень в процентах для <@{list_of_responses[i][0]}>: {sounds[i]}" + "%")


@bot.event
async def on_ready():
    print(f'Залогинился как {bot.user}')


@bot.slash_command(name='povtor', description='Повторит за тобой хуйню')
async def povtor(ctx, arg):
    await ctx.respond(arg)


@bot.command()
async def stop_recording(ctx):
    if ctx.guild.id in connections:  # Check if the guild is in the cache.
        vc = connections[ctx.guild.id]
        vc.stop_recording()  # Stop recording, and call the callback (once_done).
        del connections[ctx.guild.id]  # Remove the guild from the cache.
        await ctx.delete()  # And delete.
    else:
        await ctx.respond("Я не слушаю сейчас здесь.")  # Respond with this if we aren't recording.


@bot.slash_command(name='join', description='Will join and listen')
async def join(ctx):
    voice = ctx.author.voice

    if not voice:
        await ctx.respond('Ебень зайди в канал.')

    else:
        vc = await voice.channel.connect()
        connections.update({ctx.guild.id: vc})
        await ctx.respond('Я зашёл, слушаю.')

        vc.start_recording(
            discord.sinks.MP3Sink(),
            once_done,
            ctx.channel
        )


bot.run(key)
