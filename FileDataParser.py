from abc import ABC, abstractmethod
import time
import os

class FileDataParser(ABC):

    def __init__(self, filePath,backupDir="backup") -> None:
        self._file = filePath
        self._backupDir = backupDir
        os.makedirs(os.path.join(os.getcwd(),backupDir),exist_ok=True)

    def setFilePath(self, filePath) -> None:
        self._file = filePath

    @abstractmethod
    def _parse(self, file) -> list:
        pass

    def _checkIfAlreadyParsed(self) -> bool:
        cwd = os.getcwd()
        files = os.listdir(cwd)
        if self._file in files:
            return False
        return True

    def parseData(self) -> list:
        starttime = time.time()
        data = []
        if not self._checkIfAlreadyParsed():
            with open(self._file) as file:
                data = self._parse(file)
            cwd = os.getcwd()
            os.replace(os.path.join(cwd,self._file),os.path.join(cwd,self._backupDir,self._file))
        print("Data parsing took: " + str(time.time() - starttime) + " seconds")
        return data
