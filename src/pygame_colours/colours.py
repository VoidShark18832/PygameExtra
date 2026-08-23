import re
import pygame


# All Pygame colour names
COLOURS = pygame.colordict.THECOLORS



PARTS = [
    "alice",
    "antique",
    "aqua",
    "marine",
    "white",
    "aqua",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanched",
    "almond",
    "blue",
    "violet",
    "brown",
    "burly",
    "wood",
    "cadet",
    "chartreuse",
    "chocolate",
    "coral",
    "flower",
    "corn",
    "silk",
    "crimson",
    "cyan",
    "dark",
    "gold",
    "golden",
    "rod",
    "gray",
    "grey",
    "green",
    "khaki",
    "magenta",
    "olive",
    "orange",
    "orchid",
    "red",
    "salmon",
    "sea",
    "slate",
    "turquoise",
    "deep",
    "pink",
    "sky",
    "dim",
    "dodger",
    "firebrick",
    "floral",
    "forest",
    "fuchsia",
    "gainsboro",
    "ghost",
    "honey",
    "dew",
    "hot",
    "indian",
    "indigo",
    "ivory",
    "lavender",
    "blush",
    "lawn",
    "lemon",
    "chiffon",
    "light",
    "steel",
    "linen",
    "lime",
    "medium",
    "purple",
    "spring",
    "midnight",
    "mint",
    "cream",
    "misty",
    "rose",
    "moccasin",
    "navajo",
    "navy",
    "old",
    "lace",
    "drab",
    "pale",
    "papaya",
    "whip",
    "peach",
    "puff",
    "plum",
    "powder",
    "rosy",
    "royal",
    "saddle",
    "sandy",
    "shell",
    "sienna",
    "silver",
    "snow",
    "tan",
    "teal",
    "thistle",
    "tomato",
    "wheat",
    "smoke",
    "yellow",
]


# Remove duplicates while preserving order.
PARTS = list(dict.fromkeys(PARTS))


def split_colour(name):
    """Split a colour name into words and a possible number."""

    # Separate a number from the end.
    match = re.match(r"^([a-z]+)(\d*)$", name.lower())

    if not match:
        return [name], ""

    word = match.group(1)
    number = match.group(2)

    found_parts = []

    # Try longest words first.
    sorted_parts = sorted(PARTS, key=len, reverse=True)

    while word:
        found = False

        for part in sorted_parts:
            if word.startswith(part):
                found_parts.append(part)
                word = word[len(part):]
                found = True
                break

        if not found:
            # Keep anything unknown as one word.
            found_parts.append(word)
            break

    return found_parts, number


def make_abbreviation(name, used_abbreviations):
    """
    Create a short abbreviation.

    Rules:

    1. Try the first letter of every word.
       steelblue       -> SB
       darksteelblue   -> DSB
       lightsteelblue  -> LSB
       aquamarine      -> AM

    2. If that abbreviation already exists:
       Use 2 letters from the first word and
       1 letter from every following word.
       steelblue -> StB

    3. If that still conflicts, keep extending
       the first word until it becomes unique.

    4. Numbers are always kept at the end.
       steelblue2 -> SB2
    """

    parts, number = split_colour(name)

    # ---------------------------------------------------------
    # FIRST ATTEMPT:
    # First letter of every word.
    # ---------------------------------------------------------

    abbreviation = "".join(
        part[0].upper()
        for part in parts
    ) + number

    if abbreviation not in used_abbreviations:
        return abbreviation

    # ---------------------------------------------------------
    # SECOND ATTEMPT:
    # 2 letters from first word,
    # 1 letter from every following word.
    #
    # steelblue -> StB
    # darksteelblue -> DaSB
    # ---------------------------------------------------------

    if len(parts) > 1:
        first_length = 2
    else:
        first_length = 3

    while True:

        abbreviation = parts[0][:first_length].capitalize()

        for part in parts[1:]:
            abbreviation += part[0].upper()

        abbreviation += number

        if abbreviation not in used_abbreviations:
            return abbreviation

        # -----------------------------------------------------
        # THIRD ATTEMPT:
        # Keep extending the first word.
        #
        # If DaSB is taken:
        # DarSB
        # DarkSB
        # etc.
        # -----------------------------------------------------

        if first_length < len(parts[0]):
            first_length += 1
            continue

        # -----------------------------------------------------
        # LAST RESORT:
        # Gradually use more letters from all words.
        # -----------------------------------------------------

        max_length = max(len(part) for part in parts)

        for length in range(2, max_length + 1):

            abbreviation = "".join(
                part[:length].capitalize()
                for part in parts
            ) + number

            if abbreviation not in used_abbreviations:
                return abbreviation

        # This should only happen if the colour name
        # is completely identical to another colour name.
        return abbreviation


# =============================================================
# Generate abbreviations
# =============================================================

abbreviations = {}

for colour in COLOURS:

    abbreviation = make_abbreviation(
        colour,
        abbreviations
    )

    if abbreviation in abbreviations:
        print(
            f"WARNING: {abbreviation} is used by both "
            f"{abbreviations[abbreviation]} and {colour}"
        )
    else:
        abbreviations[abbreviation] = colour


# =============================================================
# Generate Python code
# =============================================================
user_input = input("")
if user_input == "":
    print("from typing import Final")
    print("import pygame")
    print()

    for abbreviation, colour in abbreviations.items():

        print(
            f'{abbreviation}: Final[pygame.Color] = '
            f'pygame.Color("{colour}")'
        )
if user_input == "web":
    file = open("output.txt", "w")
    for abbreviation, colour in abbreviations.items():
        file.write(f"{abbreviation} = {colour}\n")
        file.write("\n")
    file.close()