from main import *
from pathlib import Path

app.config.update(
    APPLICATION_ROOT=".",
    SERVER_NAME="elpekenin.dev",
)

print("Creating static HTMLs")

Path("static/html/40dex/").mkdir(parents=True, exist_ok=True) # create output dir if doesn't exist already

with app.app_context():
    for i in range(1, 9):
        get_40dex_page(i)
        print(f"==> Finished 40dex/{i}.html")

    get_40dex_stats_page()
    print("==> Finished 40dex/stats.html")

print("==> ==> Done")
