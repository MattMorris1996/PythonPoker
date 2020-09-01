import pickle

file = open('all_hands.obj', 'rb')
all_val = pickle.load(file)

print(len(all_val))