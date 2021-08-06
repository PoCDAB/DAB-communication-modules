#!/usr/bin/python
import os.path
import subprocess
import threading

from util.Util import Util


class ProcessThread(threading.Thread):
    def __init__(self, command, success_list, failed_list, verbose=False):
        super().__init__()
        self.command = command
        self.success_list = success_list
        self.failed_list = failed_list
        self.verbose = verbose
        self.cause = -1
        self.result = False
        self.running = True

    def can_run(self):
        file = self.command[0]
        if os.path.isfile(self.command[0]):
            self.vprint("We can run", file)
            return True
        self.vprint("Can't find", file)
        return False

    def vprint(self, *rgs, **kwrgs):
        # debug / verbose print function
        if self.verbose:
            print(" ".join(map(str, rgs)), **kwrgs)

    def stop(self):
        self.running = False

    def run(self):
        # capture output and merge error output with normal output
        print("Running command:", self.get_formatted_command())
        if not self.can_run():
            return False

        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # act according to process output
        process_output = ""
        while self.running:
            output_line = process.stdout.readline()
            if output_line == "" and process.poll() is not None:
                print("Unknown process exit method.")
                break

            if not output_line:
                print("Process stopped:", self.getName())
                break

            output_line = output_line.decode().strip()
            process_output += output_line + "\n"
            self.vprint(f"{self.getName()}: {output_line}")

            self.cause = Util.get_matching_index(self.success_list, output_line)
            if self.cause != -1:
                self.result = True
                self.vprint("Success.")
                break

            self.cause = Util.get_matching_index(self.failed_list, output_line)
            if self.cause != -1:
                self.result = False
                self.vprint("Failed.")
                break

        self.vprint("Killing process:", self.getName())
        Util.kill_process(process)
        return self.result

    def get_formatted_command(self):
        result = ""
        for x in self.command:
            result += x.replace(" ", "\\ ") + " "
        return result[:-1]
