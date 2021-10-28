#!/usr/bin/python

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
