import asyncio
import os
from pathlib import Path
import shutil
import argparse
import logging

def parse_arguments():
    parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument("source_folder", type=str, help="Шлях до вхідої папки")
    parser.add_argument("output_folder", type=str, help="Шлях до вихідної папки ")
    return parser.parse_args()

async def init_paths(source_folder, output_folder):
    source_path = Path(source_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    return source_path, output_path

async def read_folder(source_path, output_path):
    for root, dirs, files in os.walk(source_path):
        for file in files:
            file_path = Path(root) / file
            await copy_file(file_path, output_path)

async def copy_file(file_path, output_path):
    ext = file_path.suffix[1:]  # get the file extension without the dot
    target_dir = output_path / ext
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / file_path.name
    await asyncio.to_thread(shutil.copy, file_path, target_path)

def setup_logging():
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    args = parse_arguments()
    source_path, output_path = await init_paths(args.source_folder, args.output_folder)
    await read_folder(source_path, output_path)

if __name__ == "__main__":
    setup_logging()
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An error occurred: {e}")