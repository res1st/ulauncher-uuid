import re

argPattern = re.compile(r"(\d*)(.)$")


class Arguments:

    def __init__(self, arguments):

        try:
            result = argPattern.match(arguments)
            self.seperator = result.group(2)
            self.count = int(result.group(1))
        except (Exception,):
            self.seperator = None
            self.count = 1


