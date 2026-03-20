import art
print(art.banner)

is_game_on = True

MORSE_CODE = {
    "A": ".-",    "B": "-...",  "C": "-.-.",  "D": "-..",   "E": ".",
    "F": "..-.",  "G": "--.",   "H": "....",  "I": "..",    "J": ".---",
    "K": "-.-",   "L": ".-..",  "M": "--",    "N": "-.",    "O": "---",
    "P": ".--.",  "Q": "--.-",  "R": ".-.",   "S": "...",   "T": "-",
    "U": "..-",   "V": "...-",  "W": ".--",   "X": "-..-",  "Y": "-.--",
    "Z": "--..",
}

while is_game_on:
    morse_code_text = ""
    user_text = input("Enter the text input you want to convert in to morse code: ").upper()
    for char in user_text:
        if char in MORSE_CODE:
            morse_code_text += MORSE_CODE[char] + " "
        else:
            print(f"'{char}' is not supported — only letters are allowed!")

    print(f"Morse Code: {morse_code_text.strip()}")
    print()

    play_again = input("Want to translate more text? Type 'Yes' or 'No': ").lower()
    if play_again != "yes":
        print("Good Bye!")
        is_game_on = False