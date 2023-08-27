import os
import subprocess
import time


def run_command_with_output(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True
    )

    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())

    return process.poll()


def transcribe(title, model="base", output_path="./data/raw"):
    audio_path = f"""data/audio/"{title}.wav" """

    start = time.time()
    os.makedirs(f"{output_path}/{title}", exist_ok=True)
    cmd = [f"""whisper {audio_path} --model {model} -o {output_path}/"{title}" """]
    print(cmd)
    run_command_with_output(cmd)
    print(f"{title.upper()} Finished in {time.time()-start}")
    print()

    return 0
