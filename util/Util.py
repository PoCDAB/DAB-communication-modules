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

import psutil

class Util:
    @staticmethod
    def kill_process(process):
        try:
            process = psutil.Process(process.pid)
            for proc in process.children(recursive=True):
                try:
                    proc.stop()
                except AttributeError:
                    pass
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

    @staticmethod
    def get_formatted_command(command):
        result = ""
        for x in command:
            result += x.replace(" ", "\\ ") + " "
        return result[:-1]
