import subprocess
import glob
import os
import platform
from tqdm import tqdm


def DecompileBinary(path = "original_bin/"):
    def ExtractTar(tar_path):
        subprocess.run(["tar", "-xf", tar_path])

    def RunYAGL(path, yagl_path):
        if platform.system() == 'Windows':
            # print(f'Decompiling {path} via WSL...')
            subprocess.run(["powershell", "wsl", "../../run_yagl.sh", yagl_path ,path])
        elif platform.system() == "Linux":
            # print(f'Decompiling {path} via WSL...')
            subprocess.run(["../../run_yagl.sh", "../../yagl" ,path])
        else:
            print("wtf is this OS?")
            exit(1)

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

        with tqdm(total=total, desc="Processing", bar_format="{l_bar}{bar:40}{r_bar}") as pbar:
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
        print("Decompile failed. Please check the error message above.\n Do you have WSL installed?")