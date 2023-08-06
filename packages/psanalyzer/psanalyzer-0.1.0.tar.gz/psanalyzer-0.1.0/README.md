# psanalyzer

This tool supports 2 commands:
- `build` - it walks current work dir recursively, finds all files and dirs, calculates their hash and collects various info about every file/dir. Output is sqlite3 database.
  - Default db path is `${PWD}/psanalyzer.sqlite3`. You can open it with any sqlite3 tool and query it by yourself.
- `query` - it runs hardcoded SQL queries against sqlite3 database.
  - run `psanalyzer query --help` to get a list of supported queries

Example:
```bash
$ cd project
$ psanalyzer build
   Total files found: 2056
    Total dirs found: 333
    Processing files: 100%|██████████████████████████████████████████| 2056/2056 [00:00<00:00, 6991.67files/s]
     Processing dirs: 100%|█████████████████████████████████████████████| 333/333 [00:00<00:00, 7816.48dirs/s]
Success! Now run queries:
psanalyzer query duplicates --format csv > output.csv

$ psanalyzer query duplicates --format csv
path,hash,size_bytes,type
.venv\Scripts\pip.exe,314bc6d461c15eab5ce073d44e735efceb8ac76f6182e626effd20f56a97ee47,108412,file
.venv\Scripts\pip3.10.exe,314bc6d461c15eab5ce073d44e735efceb8ac76f6182e626effd20f56a97ee47,108412,file
.venv\Scripts\pip3.exe,314bc6d461c15eab5ce073d44e735efceb8ac76f6182e626effd20f56a97ee47,108412,file
.venv\Scripts\pip-3.10.exe,314bc6d461c15eab5ce073d44e735efceb8ac76f6182e626effd20f56a97ee47,108412,file
.venv\Scripts\wheel.exe,2908e4480db497f164d0a157b62baa8f8875a5f5f192f2c3337b1b0654581386,108399,file
.venv\Scripts\wheel3.10.exe,2908e4480db497f164d0a157b62baa8f8875a5f5f192f2c3337b1b0654581386,108399,file
.venv\Scripts\wheel3.exe,2908e4480db497f164d0a157b62baa8f8875a5f5f192f2c3337b1b0654581386,108399,file
.venv\Scripts\wheel-3.10.exe,2908e4480db497f164d0a157b62baa8f8875a5f5f192f2c3337b1b0654581386,108399,file
.venv\Lib\site-packages\setuptools\cli.exe,75f12ea2f30d9c0d872dade345f30f562e6d93847b6a509ba53beec6d0b2c346,65536,file
.venv\Lib\site-packages\setuptools\cli-32.exe,75f12ea2f30d9c0d872dade345f30f562e6d93847b6a509ba53beec6d0b2c346,65536,file
.venv\Lib\site-packages\setuptools\gui-32.exe,5c1af46c7300e87a73dacf6cf41ce397e3f05df6bd9c7e227b4ac59f85769160,65536,file
.venv\Lib\site-packages\setuptools\gui.exe,5c1af46c7300e87a73dacf6cf41ce397e3f05df6bd9c7e227b4ac59f85769160,65536,file
.venv\Lib\site-packages\setuptools\_vendor\packaging\specifiers.py,fb76a36790a442b8cd5b91fc34f8ef095d91060afec3dc1c60175bf248cf05f8,39046,file
........
```

- Does not depend on GIT.
- Cross-platform. If something doesn't work it's a bug.
