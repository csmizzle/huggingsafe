"""
Admin CLI for handling project level things
"""
from fire import Fire
from pathlib import Path
import os

DATA_DIR = str(Path().cwd())+"/hugging/data"


class AdminCLI:

    def clean_data(self) -> None:
        print('[!] Cleaning scraped data ...')
        for file in os.listdir(DATA_DIR):
            path_ = os.path.join(DATA_DIR, file)
            print(f'[!] Removing {path_} ...')
            os.remove(path_)


if __name__ == "__main__":
    Fire(AdminCLI)