from .utils import *

def get_home_path():
    if "HOMEPATH" in os.environ: # Windows
        HOME_ = os.environ["HOMEPATH"]
    elif "HOME" in os.environ:
        HOME_ = os.environ["HOME"] # Linux
    else:
        raise Exception('please check how to access your OS home path')    
    return HOME_

def manage_dirs(**kwargs):
    WORKSPACE_NAME = kwargs['WORKSPACE_NAME'] if 'WORKSPACE_NAME' in kwargs else "kero.projects.ws"
    WORKSPACE_DIR = kwargs['WORKSPACE_DIR'] if 'WORKSPACE_DIR' in kwargs else None
    if WORKSPACE_DIR is None:
        HOME_ = get_home_path()
        WORKSPACE_DIR =  os.path.join(HOME_, "Desktop", WORKSPACE_NAME) 
        # we put it on the Desktop for no particular reason
    if not os.path.exists(WORKSPACE_DIR):
        print(f'Setting up workspace at {WORKSPACE_DIR}')
    else:
        print(f'Current workspace: {WORKSPACE_DIR}')
    os.makedirs(WORKSPACE_DIR,exist_ok=True)

    TMP_DIR = os.path.join(WORKSPACE_DIR,'_tmp_')
    os.makedirs(TMP_DIR,exist_ok=True)    

    DIRS = {
        'WORKSPACE_DIR': WORKSPACE_DIR,
        'TMP_DIR': TMP_DIR,
    }

    """ 
    ======= customization =======
    Customize your DIRS freely, for example:
    DIRS = manage_dirs(**kwargs)
    DIRS = manage_dirs_data(DIRS, **kwargs)
    DIRS = manage_dirs_(DIRS, **kwargs)
    """
    
    return DIRS