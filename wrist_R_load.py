import pickle

def load_wrist_R_name():
    with open( 'wrist_R_name.pkl', 'rb') as f:
        return pickle.load(f)

def load_wrist_R_detect():
    with open( 'wrist_R_detect.pkl', 'rb') as f:
        return pickle.load(f)

def load_wrist_R_axis():
    with open( 'wrist_R_axis.pkl', 'rb') as f:
        return pickle.load(f)

def load_wrist_R_to_draw():
    with open( 'wrist_R_to_draw.pkl', 'rb') as f:
        return pickle.load(f)