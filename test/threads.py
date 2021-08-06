#!/usr/bin/python
import subprocess
import sys
import threading
import time

import psutil


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

    def kill(self):
        self.running = False

    def run(self):
        # capture output and merge error output with normal output
        print("Running command:", self.get_formatted_command())
        process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # act according to process output
        process_output = ""
        while self.running:
            output_line = process.stdout.readline()
            if output_line == "" and process.poll() is not None:
                print("Unknown process exit method.")
                break

            if not output_line:
                continue

            output_line = output_line.decode().strip()
            process_output += output_line + "\n"
            if self.verbose:
                print(output_line)

            self.cause = self.get_matching_index(self.success_list, output_line)
            if self.cause != -1:
                self.result = True
                print("Success!")
                break

            self.cause = self.get_matching_index(self.failed_list, output_line)
            if self.cause != -1:
                self.result = False
                print("Failed!")
                break

        if self.verbose:
            print("Killing process.")
        self._kill_process(process)
        return self.result

    def get_formatted_command(self):
        result = ""
        for x in self.command:
            result += x.replace(" ", "\\ ") + " "
        return result[:-1]

    @staticmethod
    def _kill_process(process):
        try:
            process = psutil.Process(process.pid)
            for proc in process.children(recursive=True):
                proc.stop()
            process.kill()
        except psutil.NoSuchProcess:
            print("Process already killed.")

    @staticmethod
    def get_matching_index(string_list, line):
        """
        :param string_list: A list of strings.
        :param line: The line an item in the list should contain.
        :return: The index of the matching line, otherwise -1.
        """
        index = 0
        for string in string_list:
            if string in line:
                return index
            index += 1
        return -1


# Create new threads

command1 = ["ping", "google.com"]
process1 = ProcessThread(command=command1,
                         success_list=["completed Tutorial Island"],
                         failed_list=["Response: DISABLED", "Stopped"],
                         verbose=True)
command2 = ["sleep", "5"]
process2 = ProcessThread(command=command2,
                         success_list=["completed Tutorial Island"],
                         failed_list=["Response: DISABLED", "Stopped"],
                         verbose=True)

count = 0
try:
    process1.start()
    process2.start()
    while True:
        time.sleep(1)
        count += 1
        print("Seconds:", count)
except:
    process1.kill()
    process2.kill()
    print("Stopped")
