from .utils import *

def get_df(n, selection="01", **kwargs):
    if selection=="01":
        return get_df01(n,**kwargs)
    else:
        raise NotImplementedError("Selection not available")

def get_df01(n,**kwargs):
    df = {
        'x1': np.random.normal(0,1,size=(n,)),
        'x2': np.random.normal(10,1,size=(n,)),
        'x3': np.random.normal(5,4,size=(n,)),
        't1': np.random.choice([1,2], size=(n,)),
        't2': np.random.choice([3,4,5], size=(n,)),
        'target': np.zeros(shape=(n,)),
    }
    df['target'] = (df['t1']==1).astype(int) + (df['t2']==3).astype(int) + (df['x3']>6).astype(int) + (df['x2']<1.4).astype(int)
    df = pd.DataFrame(df)
    return df
