import argparse

def test_dummy_df(parser):
    parser.add_argument('--n', default=77, type=int, help=None)
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)  # is a dictionary    

    import kero
    df = kero.dummy.get_df(n, selection="01", **kwargs)
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
