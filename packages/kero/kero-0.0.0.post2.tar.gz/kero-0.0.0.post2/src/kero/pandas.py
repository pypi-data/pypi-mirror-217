from .utils import *
import subprocess, random

def count_number_of_rows(CSV_DIR):
    # num_rows includes header(s), if any
    # this seems to be the fastest row counting alternative
    with open(CSV_DIR, 'r') as f:
        num_rows = sum(1 for _ in f)
    return num_rows

class dfProxy():
    def __init__(self):
        super(dfProxy, self).__init__()
        self.n = None
        
    def random_sample_csv(self, CSV_DIR, sample_size=1, header_lines=1):
        if self.n is None:
            self.n = count_number_of_rows(CSV_DIR) - header_lines
        skip = random.sample(range(header_lines, self.n),self.n - sample_size)
        df_sample = pd.read_csv(CSV_DIR, skiprows=skip)
        return df_sample