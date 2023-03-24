import pickle

def load_ped_zone_detect():
    with open( 'Ped_zone_detect.pkl', 'rb') as f:
        return pickle.load(f)

def load_ped_axis():
    with open( 'Ped_axis.pkl', 'rb') as f:
        return pickle.load(f)