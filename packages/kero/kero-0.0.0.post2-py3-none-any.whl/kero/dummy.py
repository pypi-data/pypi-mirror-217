from .utils import *

def get_random_dataframe(n, selection="01", **kwargs):
    if selection=="01":
        return get_df01(n,**kwargs)
    elif selection=='02':
        return get_df02(n,**kwargs)
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


def get_df02(n,nx=2,nt=3,**kwargs):
    df = {}
    df['target'] =  np.zeros(shape=(n,))
    _key_ = np.random.choice(range(2,10))
    for i in range(nx):
        mean = np.random.normal(0,100.)
        sd = np.random.uniform(0.1,10.)
        df[f'x{i}'] = np.random.normal(mean,sd,size=(n,))
        if np.random.uniform(0,1)>0.5:
            df['target'] = df['target'] + df[f'x{i}']
        else:     
            df['target'] = df['target'] - (df[f'x{i}'])**2 
    for j in range(nt):
        cmin = np.random.choice(range(-100,100))
        cmax = cmin + np.random.choice(range(1,1000))
        choices = list(range(cmin, cmax))
        df[f't{j}'] = np.random.choice(choices, size=(n,))
        if np.random.uniform(0,1)>0.5:
            df['target'] = df['target'] * df[f't{j}']
        else:     
            df['target'] = df['target'] / (df[f't{j}']**2+ 0.01 ) 
    df['target'] = np.round(df['target']).astype(int)%_key_
    df = pd.DataFrame(df)
    return df