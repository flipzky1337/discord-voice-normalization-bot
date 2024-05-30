# import numpy as np
# import soundfile as sf
# from scipy.io.wavfile import read
#
# f = sf.SoundFile('295218314400235529.wav')
# print(f.frames)
# samprate, wavdata = read('295218314400235529.wav')

from pydub import AudioSegment
import glob, os, statistics, math


def get_dbfs():
    list = []
    cnt = 1
    os.chdir('C:/Users/mosina/PycharmProjects/discord-voice-normalization-bot/recordings')
    for file in glob.glob('*.mp3'):
        audio = AudioSegment.from_file(file).dBFS
        list.append((file[0:len(file) - 4], audio))
        cnt += 1
        os.remove(file)

    penile = i_hate_math(list)

    return list, penile


def i_hate_math(ListDbfs):
    timedlist = [x[1] for x in ListDbfs]
    print(timedlist)
    array_of_perc = []
    med = statistics.median(timedlist)
    perc_med = math.pow(10, med / 10)
    for i in timedlist:
        j = math.pow(10, i / 10) / perc_med * 100
        if 0 <= j <= 200:
            array_of_perc.append(round(200 - j))
        if j > 200:
            array_of_perc.append('Ты слишком громкий, бро.')
        if j < 0:
            array_of_perc.append('Ты слишком тихий, бро.')

    return array_of_perc


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
