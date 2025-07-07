#!/usr/bin/env python

from pathlib import Path
import shutil
import subprocess as sp
import urllib.request

formula_url = "https://raw.githubusercontent.com/Homebrew/homebrew-core/refs/heads/main/Formula/c/curl.rb"

def download_file(url: str, output_path: Path):
    temp_path, _ = urllib.request.urlretrieve(url)
    shutil.copyfile(temp_path, output_path)
    
new_formula_path = Path.cwd() / "Formula" / "curl.rb"
old_formula_path = Path.cwd() / "curl_upstream.rb"
if not old_formula_path.is_file():
    download_file(formula_url, old_formula_path)

# TODO: don't run if version hasn't changed

with old_formula_path.open("r") as infile:
    with new_formula_path.open("w") as outfile:
        for line in infile:
            print(line, file=outfile, end="")
            if line.strip() == 'depends_on "zstd"':
                print(f'  depends_on "c-ares"', file=outfile)
            elif "--with-libssh2" in line.strip():
                print(f"      --with-ares", file=outfile)
