import pickle

def load_back_zone_obj():
    with open( 'back_zones.pkl', 'rb') as f:
        return pickle.load(f)

def load_obj_backzone_names():
    with open( 'back_zone_names.pkl', 'rb') as f:
        return pickle.load(f)

