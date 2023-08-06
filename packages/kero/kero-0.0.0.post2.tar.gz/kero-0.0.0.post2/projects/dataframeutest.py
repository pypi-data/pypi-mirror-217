"""
Sometimes your CSV file is just too large to load efficiently into pandas dataframe.
Let's split them into processed chunks.

Pros: should be more efficient
Cons: requires a memory space approx equal to the main data to store data in persistent memory


=== usage ===
python dataframeutest.py
python dataframeutest.py --mode save_dataframe
python dataframeutest.py --mode random_sample_csv
python dataframeutest.py --mode verify_random_sample_csv
"""
import os, argparse

def save_dataframe(parser):
    parser.add_argument('--n', default=107, type=int, help=None)
    parser.add_argument('--nx', default=11, type=int, help=None)
    parser.add_argument('--nt', default=7, type=int, help=None)
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary

    from kero.directory import manage_dirs
    DIRS = manage_dirs(**kwargs)

    from kero.dummy import get_random_dataframe
    df = get_random_dataframe(kwargs['n'],nx=kwargs['nx'],nt=kwargs['nt'], selection="02")
    df.to_csv(os.path.join(DIRS['TMP_DIR'],'dataframeutest.csv'), index=False)

def random_samples_from_csv(parser):
    parser.add_argument('--s', default=10, type=int, help=None)
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary

    from kero.directory import manage_dirs
    DIRS = manage_dirs(**kwargs)

    DATA_FRAME_DIR = os.path.join(DIRS['TMP_DIR'],'dataframeutest.csv')

    from kero.pandas import dfProxy, count_number_of_rows
    nrows = count_number_of_rows(DATA_FRAME_DIR)
    print('n rows, including header(s):', nrows)

    dfp = dfProxy()
    print(dfp.random_sample_csv(DATA_FRAME_DIR, sample_size=10, header_lines=1))

def verify_random_samples_from_csv():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=None)
    parser.add_argument('--n', default=17, type=int, help=None)
    parser.add_argument('--s', default=7, type=int, help=None)
    parser.add_argument('--repeat', default=100, type=int, help=None)
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary

    from kero.directory import manage_dirs
    DIRS = manage_dirs(**{})

    n = kwargs['n']
    s = kwargs['s']

    import pandas as pd
    import numpy as np
    from kero.pandas import dfProxy
    print(f'total size:{n} | each draw size:{s}')

    def verify_once():
        dfp = dfProxy()    

        CSV_DIR=os.path.join(DIRS['TMP_DIR'],'dataframeVRStest.csv')
        df = pd.DataFrame({'x':np.arange(n)})
        df.to_csv(CSV_DIR, index=False)

        groundtruth = set(range(n))

        tester = []
        counter = 0
        print('sizes:', end=' ')
        while True:
            samples = dfp.random_sample_csv(CSV_DIR, sample_size=s, header_lines=1)
            tester = list(tester)
            tester = tester + list(samples['x'])
            tester = set(tester)
            print(len(tester), end=' ')
            counter+=1
            if tester == groundtruth : break
        print(f"<< [{counter}]")
    
    for _ in range(kwargs['repeat']):
        verify_once()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=None)
    parser.add_argument('-m','--mode', default=None, type=str, help=None)
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary

    if kwargs['mode'] is None:
        import kero
        try:
            print('kero:', kero.__version__)
        except:
            print("You're probably using local kero repository")

    elif kwargs['mode'] == 'save_dataframe':
        save_dataframe(parser)
    elif kwargs['mode'] == 'random_sample_csv':
        random_samples_from_csv(parser)
    elif kwargs['mode'] == 'verify_random_sample_csv':
        verify_random_samples_from_csv()
    else:
        raise NotImplementedError('invalid mode?')
