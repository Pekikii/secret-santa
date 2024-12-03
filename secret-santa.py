import random
import os
import logging

logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="[%(asctime)s - %(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler()                  # Log to console
    ]
)

script_dir = os.path.dirname(__file__)

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


def save_matches_to_files(matches, dir_path):
    """
    Saves Secret Santa matches to individual files in a directory.
    
    :param matches: Dictionary of giver -> receiver pairs
    :param directory: Directory where files will be saved
    """
    os.makedirs(dir_path, exist_ok=True)
    
    # Calculate the length of the longest name
    max_length = max(len(receiver) for receiver in matches.values())
    
    for giver, receiver in matches.items():
        content = receiver.ljust(max_length)  # Pad the receiver name to the longest name length
        file_path = os.path.join(dir_path, f"{giver}.txt")
        with open(file_path, "w") as file:
            file.write(content)
    logging.info("All matches saved to individual files in '%s'.", dir_path)


if __name__ == "__main__":

    participant_names = []
    script_dir = os.path.dirname(__file__)
    input_path = os.path.join(script_dir, "participant_names.txt")
    output_path = os.path.join(script_dir, "matching")

    try:
        with open(input_path, 'r') as file:
            participant_names = [line.strip() for line in file if line.strip()]
        logging.info("Loaded %d participant names: %s", len(participant_names), participant_names)
    except FileNotFoundError:
        logging.error("The file '%s' was not found. Please create it and add participant names.", input_path)
        exit(1)

    try:
        pairs = secret_santa(participant_names)
        save_matches_to_files(pairs, output_path)
        logging.info("Secret Santa matching process completed successfully.")
    except ValueError as e:
        logging.error("Error in Secret Santa matching: %s", e)
        exit(1)
