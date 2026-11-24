import json
import os
import sys

# Enable ANSI colors on Windows and UTF-8 output for box-drawing characters
if os.name == "nt":
    os.system("")
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# File configuration using os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "songs.json")
MOODS = ["Happy", "Sad", "Calm", "Energetic", "Romantic", "Focused"]


# Minimalist ANSI palette: 1 accent (CYAN) + semantic status (GREEN/RED) + typography (BOLD/DIM)
class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    CYAN = "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"


def styled(text, *codes):
    return f"{''.join(codes)}{text}{Style.RESET}"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(f"\n  {styled('Press Enter to continue...', Style.DIM)}")


def print_success(message):
    print(f"  {styled('✓', Style.BOLD, Style.GREEN)} {message}")


def print_error(message):
    print(f"  {styled('✗', Style.BOLD, Style.RED)} {styled(message, Style.RED)}")


def print_info(message):
    print(f"  {styled('•', Style.DIM)} {styled(message, Style.DIM)}")


def print_section_header(title):
    width = max(len(title) + 4, 44)
    border = styled("─" * width, Style.DIM)
    print(f"\n{border}")
    print(f"  {styled(title.upper(), Style.BOLD, Style.CYAN)}")
    print(f"{border}")


# --- File I/O (using os) ---

def load_songs():
    if not os.path.exists(DATA_FILE):
        return []

    file_name = os.path.basename(DATA_FILE)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            songs = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"{file_name} contains invalid JSON.") from error

    if not isinstance(songs, list):
        raise ValueError(f"{file_name} must contain a list of songs.")
    return songs


def save_songs(songs):
    directory = os.path.dirname(DATA_FILE)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(songs, file, indent=2, ensure_ascii=False)


# --- Sorting Algorithms (Bubble Sort & Recursive Merge Sort) ---

def bubble_sort(songs, key_func):
    """Iterative Bubble Sort returning a new sorted list."""
    result = list(songs)
    n = len(result)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if key_func(result[j]) > key_func(result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break
    return result


def _merge(left, right, key_func):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def recursive_sort(songs, key_func):
    """Recursive Merge Sort returning a new sorted list."""
    if len(songs) <= 1:
        return list(songs)
    mid = len(songs) // 2
    left = recursive_sort(songs[:mid], key_func)
    right = recursive_sort(songs[mid:], key_func)
    return _merge(left, right, key_func)


# --- Helpers & Display ---

def choose_mood():
    print(f"\n  {styled('Available Moods:', Style.BOLD)}")
    mood_items = [
        f"{styled(f'{idx}.', Style.DIM)} {mood}"
        for idx, mood in enumerate(MOODS, start=1)
    ]
    print("  " + "   ".join(mood_items))

    while True:
        raw = input(f"  {styled('Mood (name or 1-6):', Style.BOLD)} ").strip()
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(MOODS):
                return MOODS[index]
        mood = raw.title()
        if mood in MOODS:
            return mood
        print_error("Please choose a valid mood name or number (1-6).")


def find_song(songs, song_id):
    for song in songs:
        if song["id"] == song_id:
            return song
    return None


def show_songs(songs, heading="Music Library", already_sorted=False):
    print_section_header(heading)
    if not songs:
        print_info("Your music library is empty.")
        return

    if already_sorted:
        display_songs = songs
    else:
        display_songs = bubble_sort(
            songs,
            key_func=lambda item: (item["mood"].casefold(), item["title"].casefold()),
        )

    # Calculate dynamic column widths
    id_w = max(len("ID"), *(len(str(s["id"])) for s in display_songs))
    title_w = max(len("Title"), 14, *(len(s["title"]) for s in display_songs))
    artist_w = max(len("Artist"), 14, *(len(s["artist"]) for s in display_songs))
    mood_w = max(len("Mood"), 10, *(len(s["mood"]) for s in display_songs))

    def hline(left, mid, right):
        seg = (
            f"{left}"
            f"{'─' * (id_w + 2)}{mid}"
            f"{'─' * (title_w + 2)}{mid}"
            f"{'─' * (artist_w + 2)}{mid}"
            f"{'─' * (mood_w + 2)}{right}"
        )
        return styled(seg, Style.DIM)

    v = styled("│", Style.DIM)

    print(hline("╭", "┬", "╮"))
    h_id = f"{'ID':>{id_w}}"
    h_title = f"{'Title':<{title_w}}"
    h_artist = f"{'Artist':<{artist_w}}"
    h_mood = f"{'Mood':<{mood_w}}"
    header = (
        f"{v} {styled(h_id, Style.BOLD, Style.CYAN)} "
        f"{v} {styled(h_title, Style.BOLD, Style.CYAN)} "
        f"{v} {styled(h_artist, Style.BOLD, Style.CYAN)} "
        f"{v} {styled(h_mood, Style.BOLD, Style.CYAN)} {v}"
    )
    print(header)
    print(hline("├", "┼", "┤"))

    for song in display_songs:
        song_id = styled(f'{song["id"]:>{id_w}}', Style.DIM)
        title = styled(f'{song["title"]:<{title_w}}', Style.BOLD)
        artist = f'{song["artist"]:<{artist_w}}'
        mood = f'{song["mood"]:<{mood_w}}'
        print(f"{v} {song_id} {v} {title} {v} {artist} {v} {mood} {v}")

    print(hline("╰", "┴", "╯"))
    count_label = "song" if len(display_songs) == 1 else "songs"
    print(f"  {styled(f'Total: {len(display_songs)} {count_label}', Style.DIM)}")


# --- CRUD & Sort Flows ---

def add_song(songs):
    print_section_header("Add a Song")
    title = input(f"  {styled('Song title:', Style.BOLD)} ").strip()
    artist = input(f"  {styled('Artist:', Style.BOLD)} ").strip()
    if not title or not artist:
        print_error("Title and artist cannot be empty.")
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
    print_success(f'Song "{title}" added with ID {next_id}.')


def sort_songs_menu(songs):
    print_section_header("Sort Songs")
    if not songs:
        print_info("Your music library is empty.")
        return

    print(f"  {styled('Algorithm:', Style.BOLD)}")
    print(f"  {styled('[1]', Style.BOLD, Style.CYAN)} Bubble Sort {styled('(Iterative)', Style.DIM)}")
    print(f"  {styled('[2]', Style.BOLD, Style.CYAN)} Recursive Sort {styled('(Merge Sort)', Style.DIM)}")

    algo_choice = input(f"\n  {styled('Choose algorithm (1-2):', Style.BOLD)} ").strip()
    if algo_choice == "1":
        sort_fn = bubble_sort
        algo_name = "Bubble Sort"
    elif algo_choice == "2":
        sort_fn = recursive_sort
        algo_name = "Recursive Sort"
    else:
        print_error("Please choose 1 or 2.")
        return

    print(f"\n  {styled('Sort by:', Style.BOLD)}")
    print(f"  {styled('[1]', Style.BOLD, Style.CYAN)} Title (A-Z)")
    print(f"  {styled('[2]', Style.BOLD, Style.CYAN)} Artist (A-Z)")
    print(f"  {styled('[3]', Style.BOLD, Style.CYAN)} Mood (A-Z)")
    print(f"  {styled('[4]', Style.BOLD, Style.CYAN)} ID (Ascending)")

    field_choice = input(f"\n  {styled('Choose field (1-4):', Style.BOLD)} ").strip()
    sort_options = {
        "1": ("Title", lambda s: (s["title"].casefold(), s["id"])),
        "2": ("Artist", lambda s: (s["artist"].casefold(), s["title"].casefold())),
        "3": ("Mood", lambda s: (s["mood"].casefold(), s["title"].casefold())),
        "4": ("ID", lambda s: s["id"]),
    }

    if field_choice not in sort_options:
        print_error("Please choose a number from 1 to 4.")
        return

    field_name, key_func = sort_options[field_choice]
    sorted_songs = sort_fn(songs, key_func)

    clear_screen()
    show_songs(
        sorted_songs,
        heading=f"Sorted by {field_name} — {algo_name}",
        already_sorted=True,
    )


def update_song(songs):
    print_section_header("Edit a Song")
    try:
        song_id = int(input(f"  {styled('Enter the song ID to edit:', Style.BOLD)} ").strip())
    except ValueError:
        print_error("Please enter a valid number.")
        return

    song = find_song(songs, song_id)
    if song is None:
        print_error("Song not found.")
        return

    print_info("Leave a field blank to keep its current value.")
    current_title = f"[{song['title']}]"
    current_artist = f"[{song['artist']}]"
    current_mood = f"[{song['mood']}]"

    title = input(
        f"  {styled('Title', Style.BOLD)} {styled(current_title, Style.DIM)}: "
    ).strip()
    artist = input(
        f"  {styled('Artist', Style.BOLD)} {styled(current_artist, Style.DIM)}: "
    ).strip()

    song["title"] = title or song["title"]
    song["artist"] = artist or song["artist"]

    change_mood = input(
        f"  {styled('Mood', Style.BOLD)} {styled(current_mood, Style.DIM)} "
        f"{styled('(change? y/N):', Style.DIM)} "
    ).strip().lower()
    if change_mood == "y":
        song["mood"] = choose_mood()

    save_songs(songs)
    print_success("Song updated.")


def delete_song(songs):
    print_section_header("Delete a Song")
    try:
        song_id = int(input(f"  {styled('Enter the song ID to delete:', Style.BOLD)} ").strip())
    except ValueError:
        print_error("Please enter a valid number.")
        return

    song = find_song(songs, song_id)
    if song is None:
        print_error("Song not found.")
        return

    confirm = input(
        f"  {styled('Delete', Style.BOLD, Style.RED)} "
        f'"{styled(song["title"], Style.BOLD)}"? '
        f"{styled('(y/N):', Style.DIM)} "
    ).strip().lower()
    if confirm != "y":
        print_info("Deletion cancelled.")
        return

    songs.remove(song)
    save_songs(songs)
    print_success(f'Song "{song["title"]}" deleted.')


def print_menu(song_count):
    width = 44
    top = styled(f"╭{'─' * width}╮", Style.DIM)
    mid = styled(f"├{'─' * width}┤", Style.DIM)
    bot = styled(f"╰{'─' * width}╯", Style.DIM)
    v = styled("│", Style.DIM)

    title_text = "♪  MUSIC BY MOOD"
    count_label = "song" if song_count == 1 else "songs"
    subtitle_text = f"Library: {song_count} {count_label}"

    menu_items = [
        ("1", "Add a song"),
        ("2", "Show all songs (sorted by mood)"),
        ("3", "Show songs by mood"),
        ("4", "Sort songs (Bubble / Recursive)"),
        ("5", "Edit a song"),
        ("6", "Delete a song"),
        ("7", "Exit"),
    ]

    print(f"\n{top}")
    print(f"{v} {styled(f'{title_text:<{width - 2}}', Style.BOLD, Style.CYAN)} {v}")
    print(f"{v} {styled(f'{subtitle_text:<{width - 2}}', Style.DIM)} {v}")
    print(mid)
    for key, label in menu_items:
        padding = width - 2 - len(key) - 3 - len(label)
        if key == "7":
            key_str = styled(f"[{key}]", Style.BOLD, Style.RED)
            label_str = styled(label, Style.DIM)
        else:
            key_str = styled(f"[{key}]", Style.BOLD, Style.CYAN)
            label_str = label
        print(f"{v} {key_str} {label_str}{' ' * padding} {v}")
    print(bot)


def main():
    try:
        songs = load_songs()
    except ValueError as error:
        print_error(f"Could not load your music library: {error}")
        return

    while True:
        clear_screen()
        print_menu(len(songs))
        choice = input(f"  {styled('Choose an option (1-7):', Style.BOLD)} ").strip()

        if choice == "1":
            clear_screen()
            add_song(songs)
            pause()
        elif choice == "2":
            clear_screen()
            show_songs(songs, heading="All Songs (Sorted by Mood)")
            pause()
        elif choice == "3":
            clear_screen()
            print_section_header("Filter Songs by Mood")
            mood = choose_mood()
            filtered = [song for song in songs if song["mood"] == mood]
            sorted_filtered = recursive_sort(
                filtered,
                key_func=lambda item: item["title"].casefold(),
            )
            clear_screen()
            show_songs(
                sorted_filtered,
                heading=f"Songs — Mood: {mood}",
                already_sorted=True,
            )
            pause()
        elif choice == "4":
            clear_screen()
            sort_songs_menu(songs)
            pause()
        elif choice == "5":
            clear_screen()
            update_song(songs)
            pause()
        elif choice == "6":
            clear_screen()
            delete_song(songs)
            pause()
        elif choice == "7":
            clear_screen()
            print(f"\n  {styled('Goodbye! Enjoy your music ♪', Style.BOLD, Style.CYAN)}\n")
            break
        else:
            print_error("Please choose a number from 1 to 7.")
            pause()


if __name__ == "__main__":
    main()
