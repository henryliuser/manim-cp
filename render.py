import ffmpeg
import os
import sys



if __name__ == '__main__':
    path = f"{os.getcwd()}/{sys.argv[1]}"
    k = lambda x: int(x[1:-3].split('-')[0])
    A = os.listdir(path)
    A = [x for x in A if x[0] == 'p']
    A.sort(key=k)
    q = sys.argv[2]
    qmap = {'l': '480p15', 'm': '720p30', 'h': '1080p60'}
    s = "env PYTHONPATH=\"/Users/samuelbrashears/Documents/PythonProjects/manim-cp/\""
    s += f" manim -q{q} "
    os.system("mkdir output")
    for i, x in enumerate(A):
        s2 = f"{path}/{x}"
        os.system(f"{s}{s2}")
        a = x[:-3]
        b = f"p{k(x)}"
        os.system(f"cp {os.getcwd()}/media/videos/{a}/{qmap[q]}/{b}.mp4 {os.getcwd()}/output/{i}.mp4")



    # input_video = ffmpeg.input('./output/0')
    # for x in input_video

