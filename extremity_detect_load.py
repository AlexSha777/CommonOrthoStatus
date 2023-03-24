import pickle

def load_extremity_zone():
    with open( 'zone_detect.pkl', 'rb') as f:
        return pickle.load(f)

def load_extremity_axis():
    with open( 'zone_axis.pkl', 'rb') as f:
        return pickle.load(f)