import discord
import config
import voice_analysis
from voice_analysis import get_dbfs
import os

key = config.key

bot = discord.Bot()
connections = {}


# class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
#     @discord.ui.button(label="Остановить запись", style=discord.ButtonStyle.danger) # Create a button with the label "😎 Click me!" with color Blurple
#     async def button_callback(self, button, interaction):
#         await interaction.response.defer()


async def once_done(sink: discord.sinks, channel: discord.TextChannel, guild_id):
    server_audio_filepath = f"{config.recording_path}/{guild_id}/"

    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    await sink.vc.disconnect()

    os.makedirs(os.path.dirname(server_audio_filepath), exist_ok=True)

    for user_id, audio in sink.audio_data.items():
        with open(f"{server_audio_filepath}{user_id}.mp3",
                  "wb") as f:
            f.write(audio.file.getbuffer())

    # files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    await channel.send(f"Записал голос для: {', '.join(recorded_users)}.")
    list_of_responses, sounds = get_dbfs(guild_id)
    for i in range(len(list_of_responses)):
        if isinstance(sounds[i], float):
            await channel.send(f"Уровень в процентах для <@{list_of_responses[i][0]}>: {sounds[i]}" + "%")
        else:
            await channel.send(f'{sounds[i]} <@{list_of_responses[i][0]}>')


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

        async def button_callback(interaction):
            await interaction.response.defer()
            await stop_recording(ctx)

        button = discord.ui.Button(label='Остановить запись', style=discord.ButtonStyle.danger, emoji='⛔')
        view = discord.ui.View(button)
        button.callback = button_callback

        await ctx.respond('Я зашёл, слушаю.', view=view)

        vc.start_recording(
            discord.sinks.MP3Sink(),
            once_done,
            ctx.channel,
            ctx.guild.id
        )


@bot.slash_command(name='userlist', description='List of users, with percents (recalculated)')
async def userlist(ctx):
    try:
        list_of_responses, sounds = get_dbfs(ctx.guild.id)
        for i in range(len(list_of_responses)):
            await ctx.respond('Хорошо! Вот:')
            await ctx.send(f"Уровень в процентах для <@{list_of_responses[i][0]}>: {sounds[i]}" + "%")
    except:
        await ctx.respond('Произошла ошибка, возможно список записей пуст.')


@bot.slash_command(name='delete-recording', description='delete specified user\'s recording')
async def delete_user_audio_recording(ctx, arg):
    try:
        voice_analysis.delete_audio(ctx.guild.id, arg)
        await ctx.respond(f"Аудиоданные удалены для {arg}")
    except:
        await ctx.respond(f'Данные для {arg} уже были удалены')


bot.run(key)
