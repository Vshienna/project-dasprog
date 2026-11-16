
moods = ["banger", "energetic", "sad", "romantic"]
def main ():
    print(
        "==Music finder by mood==\n"
        "1. Add song\n"
        "2. Show all song\n"
        "3. Exit\n")
    pil=str(input("choose an option: "))

    if pil == "1": 
        addmusic()

def addmusic():
    print("====add music====")
    title = str(input("Title : "))
    artist = str(input("Artist : "))
    if title or artist == " ":
        print("Title or artist cannot be empty")
        return
