import subprocess
import glob
import os
import platform
import threading
import time
from tqdm import tqdm


def DecompileBinary(path = "original_bin/"):
    def ExtractTar(tar_path):
        subprocess.run(["tar", "-xf", tar_path])

    def RunYAGL(yagl_path, path, timeout_time=60):
        runparams = ["bash", "../../run_yagl.sh", yagl_path, path]
        if platform.system() == 'Windows':
            runparams = ["wsl"] + runparams
        def run_command():
            try:
                subprocess.run(runparams, timeout=timeout_time)
            except subprocess.TimeoutExpired:
                print(f"\n{path} was terminated due to timeout.")
        thread = threading.Thread(target=run_command)
        thread.start()
        pbar = tqdm(total = timeout_time, bar_format="{l_bar}{bar:40}{r_bar}" + path, desc="Timeout(s)", leave=False)
        for i in range(timeout_time):
            if not thread.is_alive():
                pbar.update(timeout_time - i)
                break
            else:
                pbar.update(1)
                time.sleep(1)

        thread.join()

        if thread.is_alive():
            print(f"\n{path} was terminated due to timeout.")

    def GetOriginalBinary(path):
        tars = [os.path.relpath(tar, path) for tar in glob.glob(f"{path}/*.tar")]
        return tars if tars else None
    
    binary_path = GetOriginalBinary(path)

    if binary_path:
        os.chdir(path)
        with tqdm(total=len(binary_path), desc="Extracting", bar_format="{l_bar}{bar:40}{r_bar}") as pbar:
            for tar in binary_path:
                ExtractTar(tar)
                pbar.update()
            # print(f"Extracted {tar}")

    for root, dirs, files in os.walk('.'):
        total = sum(len(glob.glob(f"{dir}/*.grf")) for dir in dirs) + len(glob.glob("*.grf"))

        with tqdm(total=total, desc="Processing", bar_format="{l_bar}{bar:40}{r_bar}", leave=False) as pbar:
            for dir in dirs:
                os.chdir(dir)
                for grf in glob.glob("*.grf"):
                    RunYAGL("../../yagl", grf)
                    pbar.update()  # 更新进度条
                os.chdir("..")
            grfs = glob.glob("*.grf")
            if grfs:
                for grf in grfs:
                    RunYAGL("../yagl", grf)
                    pbar.update()  # 更新进度条
        break
                

        


if __name__ == "__main__":
    
    current_dir = os.getcwd()
    print(f'Current platform: {platform.system()}\n')
    if platform.system() == 'Windows':
        print("You are running this script on Windows, please make sure you\
\nhave WSL installed and have a WSL distribution installed.\
\nThis script will run the decompilation process on WSL.\
\ngrf files will be decompiled slower than on Linux.\n")
    
    try:
        DecompileBinary()
    except Exception as e:
        print(e)
        print("Decompile failed. Please check the error message above.\nDo you have WSL installed?")