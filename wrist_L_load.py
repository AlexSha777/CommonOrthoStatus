import pickle


def load_wrist_L_name():
    with open( 'wrist_L_name.pkl', 'rb') as f:
        return pickle.load(f)

def load_wrist_L_detect():
    with open( 'wrist_L_detect.pkl', 'rb') as f:
        return pickle.load(f)

def load_wrist_L_axis():
    with open( 'wrist_L_axis.pkl', 'rb') as f:
        return pickle.load(f)

def load_wrist_L_to_draw():
    with open( 'wrist_L_to_draw.pkl', 'rb') as f:
        return pickle.load(f)