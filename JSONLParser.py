from FileDataParser import FileDataParser
import json

class JSONLParser(FileDataParser):


    def __init__(self, filePath):
        super().__init__(filePath)  

    def _parse(self, file) -> list:
        data = [json.loads(line) for line in file]
        return data
