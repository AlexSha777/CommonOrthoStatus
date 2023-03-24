import pickle

def load_obj():
    with open( 'front_zones.pkl', 'rb') as f:
        return pickle.load(f)

def load_obj_zone_names():
    with open( 'front_zone_names.pkl', 'rb') as f:
        return pickle.load(f)


if __name__ == "__main__":
    with open('front_zones.pkl', 'rb') as f:
        print(pickle.load(f).keys())
