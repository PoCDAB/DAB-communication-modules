import subprocess
def get_formatted_command(command):
    result = ""
    for x in command:
        result += x.replace(" ", "\\ ") + " "
    return result[:-1]


def run_command(command):
    print(f"Running command: {get_formatted_command(command)}")
    result = subprocess.run(command, capture_output=True)
    return result.stdout.decode()


command = ["./encryption-module", "--key", "ship-32-key", "--message", "hoischip", "--encrypt", "-v"]

encrypted_message = run_command(command)
if encrypted_message == "":
    print(f"Encryption failed with empty result: {get_formatted_command(command)}")
    quit(1)
print(encrypted_message)
