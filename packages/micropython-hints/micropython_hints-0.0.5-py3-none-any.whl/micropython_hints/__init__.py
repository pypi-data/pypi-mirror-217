import os
TGT_DIR = os.path.join(os.path.split(os.path.abspath(os.__file__))[0], "site-packages")
DIR = os.path.split(os.path.abspath(__file__))[0]

def run():
    print(f"\033[31m[WARNING]: Please note that this package will be installed at `{TGT_DIR}` in a destructive manner. \
        \n\rIt is strongly recommended to install it within a virtual environment.\033[0m", end='')

    if input("continue? [y/N]: ").strip() not in ['yes', 'Y', 'y']:
        exit()

    from tqdm import tqdm
    from shutil import copyfile
    for name in tqdm(os.listdir(DIR)):
        if name.startswith("__") and name.endswith("__"):
            continue
        fpath = os.path.join(DIR, name)
        tpath = os.path.join(TGT_DIR, name)
        copyfile(fpath, tpath)
    print("done")

def remove():
    if input("remove? [y/N]: ").strip() not in ['yes', 'Y', 'y']:
        exit()
    from tqdm import tqdm
    for name in tqdm(os.listdir(DIR)):
        if name.startswith("__") and name.endswith("__"):
            continue
        tpath = os.path.join(TGT_DIR, name)
        os.remove(tpath)
    print("done")

if __name__ == '__main__':
    ...