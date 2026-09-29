with open("index.html", "w", encoding="utf-8") as f:
    f.write(open("index.html", "r", encoding="utf-8").read())
print("Synced successfully!")
