""" Assume code is executed in "projects" folder.
python _tests01.py --TOGGLES 11
"""

import argparse

def test_dummy_df(parser):
    # python _tests01.py --TOGGLES 10
    parser.add_argument('--n', default=77, type=int, help=None)
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary    

    import kero.dummy
    df = kero.dummy.get_random_dataframe(kwargs['n'], selection="01")
    print('='*47)
    print(df)

    import kero.dummy as kdum
    df2 = kdum.get_random_dataframe(4, selection="01")
    print('\n','='*47)
    print(df2)

    from kero.dummy import get_random_dataframe
    print('\n','='*47)
    print(get_random_dataframe(2, selection="01"))

def test_dummy_df2(parser):
    # python _tests01.py --TOGGLES 01
    parser.add_argument('--n', default=77, type=int, help=None)
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary    

    from kero.dummy import get_random_dataframe
    df = get_random_dataframe(kwargs['n'],nx=2,nt=3, selection="02")
    print(df)

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=None)
    parser.add_argument('--TOGGLES', default='1', type=str, help=None)
    # parser.add_argument('-m','--mode', default=None, type=str, help=None)
    # parser.add_argument('--id', nargs='+', default=['a','b']) # for list args
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary    

    TOGGLES = kwargs['TOGGLES']
    if TOGGLES[0] == '1':
        test_dummy_df(parser)
    if len(TOGGLES)<=1: exit()
    
    if TOGGLES[1] == '1':
        test_dummy_df2(parser)
    if len(TOGGLES)<=2: exit()

