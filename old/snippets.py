def get_key(ship_id):
    ship_id = str(ship_id)
    vprint(f"Determining key for ship with id {ship_id}")
    if not exists(KEY_FOLDER):
        print(f"{KEY_FOLDER} does not exist.")
        quit(1)

    key_file = None
    for entry in os.scandir(KEY_FOLDER):
        if entry.name.startswith(ship_id):
            key_file = entry.path
            break

    if key_file is None:
        print(f"Could not find key file for ship with id {ship_id} in {KEY_FOLDER}.")
        quit(1)

    key = read_file(key_file).strip()  # otherwise a newline at end, which breaks everything (gpg invalid passphrase)
    vprint(f"Found key for ship {ship_id}: {key}")
    return key

