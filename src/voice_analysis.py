import datetime

from pydub import AudioSegment
import glob, os, statistics, math
import config


def get_dbfs(guild_id):
    list = []
    cnt = 1
    guild_recording_path = f'{config.recording_path}/{guild_id}'
    os.chdir(guild_recording_path)
    for file in glob.glob('*.mp3'):
        time_distinction = datetime.datetime.now() - datetime.datetime.fromtimestamp(os.path.getmtime(file))
        if time_distinction.days >= 2:
            os.remove(file)
        else:
            audio = AudioSegment.from_file(file).dBFS # https://github.com/jiaaro/pydub/blob/master/API.markdown#audiosegmentdbfs
            list.append((file[0:len(file) - 4], audio)) # file[:-4] чтобы убрать .mp3 в конце
            cnt += 1

    print(guild_id)

    penile = i_hate_math(list)

    return list, penile


def i_hate_math(ListDbfs):
    timedlist = [x[1] for x in ListDbfs] # dbfs из кортежей
    array_of_perc = []
    print(timedlist)
    med = statistics.median(timedlist) # берёт медиану из ВСЕХ dbfs
    perc_med = math.pow(10, med / 10) # переводит медиану из dbfs в проценты
    for i in range(len(timedlist)):
        j = math.pow(10, timedlist[i] / 10) / perc_med * 100
        if 0 <= j <= 200:
            array_of_perc.append(200 - j)
        if j > 200:
            array_of_perc.append('Ты слишком громкий, бро.')
        if j < 0:
            array_of_perc.append('Ты слишком тихий, бро.')

    return array_of_perc


def delete_audio(guild_id, user_id):
    user_recording_path = f'{config.recording_path}/{guild_id}/{user_id[2:-1]}.mp3'
    os.remove(user_recording_path)

# audio = AudioSegment.from_file('295218314400235529.wav')
# print(audio.dBFS)
#
#
# def match_target_amplitude(sound, target_dBFS):
#     change_in_dBFS = target_dBFS - sound.dBFS
#     return sound.apply_gain(change_in_dBFS)
#
# sound = AudioSegment.from_file('recordings/295218314400235529.mp3')
# normalized_sound = match_target_amplitude(sound, -20.0)
