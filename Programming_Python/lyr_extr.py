EXIT_SYMBOLS = ['e','q']
indentation_symbol = "============================================================"

from lyrics_extractor import Song_Lyrics

extract_lyrics = Song_Lyrics("GOOGLEKEY")

while True:
    song_words = input("Enter the song of your interest: ")
    if not song_words:
        print("I don't see anything that have a meaning.\nTry again (or exit with 'e')\n")
    elif song_words in EXIT_SYMBOLS:
        print('Exited Successfully')
        break
    else:
        song_title, song_lyrics = extract_lyrics.get_lyrics(song_words)
        pagination = len(indentation_symbol) - len(song_title)
        if pagination > 1:
            song_title = ' '*(pagination//2) + song_title + ' '*(pagination//2)
        print("\n============================================================", song_title, "============================================================", sep='\n', end='\n\n')
        print(song_lyrics)
        print()
        
