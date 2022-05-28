import difflib as df
import logging
import sys, os
import pathlib

PATH_FILE = pathlib.Path(__file__).parents[0]


class Differences:

    def __init__(self, file1, file2):
        self.path_one = file1
        self.path_two = file2


    @staticmethod
    def read_file(self) -> str:
        """ Helper function for reading file """
        try:
            with open(self.path_one) as f, open(self.path_two) as s:
                f1 = f.read().splitlines()
                f2 = s.read().splitlines()
                return f1, f2
                
        except OSError as err:
            msg = f"[diff]: Unable to open : {err}"
            logging.error(msg)
            sys.exit(4)
            
        finally:
            msg = f"[read_file]: files read"
            logging.debug(msg)


    @staticmethod
    def write_file(file_name: str, line: str, tmp):
        """ Helper function for writing to file """

        if tmp is None:
            with open(file_name, "a") as f:
                f.writelines(line[2:] + '\n')
            # TODO: Exception
        else:
            tmp.writelines(line[2:] + '\n')


    def diff(self):
        """ Getting differences between the contents of two files """
        
        f1, f2 = self.read_file(self)
        d = df.Differ()
        diff = d.compare(f1, f2)

        return diff


    def create_files(self, diff, dir_name, tmp1 = None, tmp2 = None):
        """
        Will produce two output files - first output file should contain
        only strings which were found in first input file, but not in the
        second one; second output file - strings found in the second input
        file, but not in the first
        """

        p_first = pathlib.Path(PATH_FILE, dir_name, "first.txt")
        p_second = pathlib.Path(PATH_FILE, dir_name, "second.txt")

        if not os.path.exists(os.path.dirname(p_first)):
            os.makedirs(dir_name)
    
        for line in diff:
            if line.startswith('-'):
                self.write_file(p_first, line, tmp1)
            elif line.startswith('+'):
                self.write_file(p_second, line, tmp2)


    def diff_in_html(self, dir_name, file_name):
        """
        Html file will be created, in which the
        lines placed in the first file will be highlighted in red;
        lines placed in the second file are highlighted in green
        """
        
        f1, f2 = self.read_file(self)
        d = df.HtmlDiff()
        diff = d.make_file(f1, f2)
        
        path_html = pathlib.Path(PATH_FILE, dir_name, file_name)

        if not os.path.exists(os.path.dirname(path_html)):
            os.makedirs(dir_name)
        
        with open(path_html, "w") as f:
            for line in diff.splitlines():
                print(line, file=f)


if __name__ == '__main__':
    """
    Will take two input files, both files consist of lexicographically
    sorted in the same order ASCII strings
    """
    
    try:   
        first = sys.argv[1]
        second = sys.argv[2]
        
    except IndexError as err:
        msg = f"[agrv]: {err}"
        logging.error(msg)
        sys.exit(3)
        
    logging.info("start")
    
    d = Differences(first, second)
    diff = d.diff()
    #print('\n'.join(list(diff)))
    d.create_files(diff, "result")
    
    #create visual file
    d.diff_in_html("result", "diff.html")

    logging.info("success")

