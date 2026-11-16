import json
from pathlib import Path


DATA_FILE = Path(__file__).with_name("songs.json")
MOODS = ["Happy", "Sad", "Calm", "Energetic", "Romantic", "Focused"]


def load_songs():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            songs = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"{DATA_FILE.name} contains invalid JSON.") from error

    if not isinstance(songs, list):
        raise ValueError(f"{DATA_FILE.name} must contain a list of songs.")
    return songs


def save_songs(songs):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(songs, file, indent=2, ensure_ascii=False)


def choose_mood():
    print("Available moods: " + ", ".join(MOODS))
    while True:
        mood = input("Mood: ").strip().title()
        if mood in MOODS:
            return mood
        print("Please choose one of the moods listed above.")


def find_song(songs, song_id):
    for song in songs:
        if song["id"] == song_id:
            return song
    return None


def show_songs(songs):
    if not songs:
        print("Your music library is empty.")
        return

    for song in sorted(songs, key=lambda item: (item["mood"].casefold(), item["title"].casefold())):
        print(
            f'ID: {song["id"]} | {song["title"]} - {song["artist"]} '
            f'| Mood: {song["mood"]}'
        )


def add_song(songs):
    print("\nAdd a song")
    title = input("Song title: ").strip()
    artist = input("Artist: ").strip()
    if not title or not artist:
        print("Title and artist cannot be empty.")
        return

    next_id = max((song["id"] for song in songs), default=0) + 1
    songs.append(
        {
            "id": next_id,
            "title": title,
            "artist": artist,
            "mood": choose_mood(),
        }
    )
    save_songs(songs)
    print("Song added.")


def update_song(songs):
    try:
        song_id = int(input("Enter the song ID to edit: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    song = find_song(songs, song_id)
    if song is None:
        print("Song not found.")
        return

    print("Leave a field blank to keep its current value.")
    title = input(f'Title [{song["title"]}]: ').strip()
    artist = input(f'Artist [{song["artist"]}]: ').strip()
    song["title"] = title or song["title"]
    song["artist"] = artist or song["artist"]
    if input(f'Mood [{song["mood"]}] (change? y/N): ').strip().lower() == "y":
        song["mood"] = choose_mood()

    save_songs(songs)
    print("Song updated.")


def delete_song(songs):
    try:
        song_id = int(input("Enter the song ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    song = find_song(songs, song_id)
    if song is None:
        print("Song not found.")
        return

    if input(f'Delete "{song["title"]}"? (y/N): ').strip().lower() != "y":
        print("Deletion cancelled.")
        return

    songs.remove(song)
    save_songs(songs)
    print("Song deleted.")


def main():
    try:
        songs = load_songs()
    except ValueError as error:
        print("Could not load your music library: {error}")
        return

    while True:
        print(
            "\n=== Music by Mood ===\n"
            "1. Add a song\n"
            "2. Show all songs (sorted by mood)\n"
            "3. Show songs by mood\n"
            "4. Edit a song\n"
            "5. Delete a song\n"
            "6. Exit"
        )
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_song(songs)
        elif choice == "2":
            show_songs(songs)
        elif choice == "3":
            mood = choose_mood()
            show_songs([song for song in songs if song["mood"] == mood])
        elif choice == "4":
            update_song(songs)
        elif choice == "5":
            delete_song(songs)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 6.")


if __name__ == "__main__":
    main()