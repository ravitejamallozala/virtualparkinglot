class FileUtility:
    """
    Utility class to load the input file
    """

    def __init__(self):
        self.file = None

    def load_file(self, filepath):
        try:
            self.file = open(filepath, 'r')
        except IOError:
            self.file = None
            print("Input File not found in given path")
