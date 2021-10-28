#
#    CFNS - Rijkswaterstaat CIV, Delft © 2020 - 2021 <cfns@rws.nl>
#
#    Copyright 2020 - 2021 Jort Stuijt <jort.stuyt@gmail.com>
#
#    This file is part of DAB-communication-modules
#
#    DAB-communication-modules is free software: you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    DAB-communication-modules is distributed in the hope that
#    it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#    warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#    See the GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with DAB-communication-modules.
#    If not, see <https://www.gnu.org/licenses/>.
#

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

