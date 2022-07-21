from os import listdir
from os import system
if __name__ == '__main__':
    k = lambda x: int(x.split('.')[0])
    a = listdir('./output')
    a.sort(key=k)
    with open('concat_names.txt', 'w') as f:
        for b in a:
            f.write(f"file './output/{b}'\n")
    system('ffmpeg -f concat -safe 0 -i concat_names.txt -c copy output.mp4')
