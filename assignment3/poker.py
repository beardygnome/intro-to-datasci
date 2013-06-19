from __future__ import absolute_import, division, print_function, unicode_literals

import json
import MapReduce

mr = MapReduce.MapReduce()

def init():
    """(NoneType) -> list of str

    Generate all 5-card poker hands as a list of comma seprated strings.
    e.g. : '3S,QC,AD,AC,7H'
    """

    faces = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K'];
    suits = ['S', 'C', 'D', 'H'] # Spades, Clubs, Diamonds, Hearts

        # Make a list of all 52 cards in the deck; e.g. '3S' or 'QH'.
    all_cards = [f + s for s in suits for f in faces];

        # Generate unique 5-card combinations (poker hands).
    all_cards_len = len(all_cards)  # 52
    all_hands = []

    for i1 in range(all_cards_len):
        for i2 in range(i1+1, all_cards_len):
            for i3 in range(i2+1, all_cards_len):
                for i4 in range(i3+1, all_cards_len):
                    for i5 in range(i4+1, all_cards_len):
                        hand = '{0},{1},{2},{3},{4}'.format(all_cards[i1],
                                all_cards[i2], all_cards[i3], all_cards[i4],
                                all_cards[i5])
                        all_hands.append(hand)

    return (all_hands, faces, suits)


def mapper(record):
    """((list of str, list of str, str)) -> (str, int)

    Take a tuple of (list of face values, list of suit values, 5-card hand) and
    return the highest made hand e.g. 'Flush', 'Pair' etc, plus a count of 1.
    """

    faces, suits, hand = record
    cards = hand.split(',')  # 5 cards like 'QH' (for Queen of Hearts)

    # Initialise counts of all faces and suits as 0
    counts = {val: 0 for val in faces + suits}

    # Get counts of all faces and suits in the 5-card hand
    for card in cards:
        face = card[0]
        suit = card[1]
        counts[face] += 1
        counts[suit] += 1

    # Flush is 5 cards of the same suit
    is_flush = ((counts['S'] == 5) or
                (counts['C'] == 5) or
                (counts['D'] == 5) or
                (counts['H'] == 5))

    is_straight = False

    # for a Straight, 'A' (ace) can be low or high, so must appear at both ends
    # of the list; use list comprehension & list concatenation
    straight_faces = [face for face in faces] + ["A"]

    # Straight is five consectutive faces
    for i in range(len(straight_faces) - 4):
        if (counts[straight_faces[i]] and
                counts[straight_faces[i+1]] and
                counts[straight_faces[i+2]] and
                counts[straight_faces[i+3]] and
                counts[straight_faces[i+4]]):
            is_straight = True
            break

    # Quads, Trips and Pairs are 4, 3 or 2 cards with the same face
    # Two Pair is two separate pairs
    is_quad, is_trip, is_pair, is_two_pair = False, False, False, False

    for face in faces:
        face_count = counts[face]

        if face_count == 4:
            is_quad = True
        elif face_count == 3:
            is_trip = True
        elif face_count == 2:
            if is_pair:
                # there is already a pair in this 5-card hand
                is_two_pair = True

            is_pair = True

    # Emit output: a count of 1 for the detected hand
    result = ""

    if is_straight and is_flush and counts["K"] and counts["A"]:
        # Straight Flush containing both King and Ace must be Royal Flush
        result = "Royal Flush"
    elif is_straight and is_flush:
        result = "Straight Flush"
    elif is_quad:
        result = "4 of a Kind"
    elif is_trip and is_pair:
        result = "Full House"
    elif is_flush:
        result = "Flush"
    elif is_straight:
        result = "Straight"
    elif is_trip:
        result = "3 of a Kind"
    elif is_two_pair:
        result = "Two Pair"
    elif is_pair:
        result = "Pair"
    else:
        result = "High Card"

    mr.emit_intermediate(result, 1)


def reducer(key, list_of_counts):
    """(str, list of int) -> NoneType

    Count up how many unique hands make the hand referenced by key.
    """

    mr.emit((key, sum(list_of_counts)))


if __name__ == "__main__":
    all_hands, faces, suits = init()

    # mapper function expects data in json format
    json_encoder = json.JSONEncoder()
    data = [json_encoder.encode((faces, suits, hand)) for hand in all_hands]

    mr.execute(data, mapper, reducer)
