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
