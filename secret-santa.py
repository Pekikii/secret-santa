import random
import os

def secret_santa(names):
    """
    Matches names for a Secret Santa exchange.
    
    :param names: List of names of participants
    :return: Dictionary mapping each person to their Secret Santa recipient
    """
    if len(names) < 2:
        raise ValueError("At least two participants are required for Secret Santa.")
    
    givers = names[:]
    receivers = names[:]
    random.shuffle(receivers)

    while any(giver == receiver for giver, receiver in zip(givers, receivers)):
        random.shuffle(receivers)

    return {giver: receiver for giver, receiver in zip(givers, receivers)}


def save_matches_to_files(matches, directory="matching"):
    """
    Saves Secret Santa matches to individual files in a directory.
    
    :param matches: Dictionary of giver -> receiver pairs
    :param directory: Directory where files will be saved
    """
    os.makedirs(directory, exist_ok=True)

    for giver, receiver in matches.items():
        file_path = os.path.join(directory, f"{giver}.txt")
        with open(file_path, "w") as file:
            file.write(receiver)


if __name__ == "__main__":
    participant_names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Florentina"
    ]
    
    try:
        pairs = secret_santa(participant_names)
        save_matches_to_files(pairs)
    except ValueError as e:
        print(f"Error: {e}")
