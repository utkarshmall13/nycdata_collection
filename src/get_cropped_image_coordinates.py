import pickle
import json
from tqdm import tqdm
import numpy as np
from sklearn.neighbors import NearestNeighbors

with open('satellite_centers.pkl', 'rb') as f:
    satellite_centers = pickle.load(f)
with open('image_data.pkl', 'rb') as f:
    image_data = pickle.load(f)

bounds_by_year = {}
with open('bounds.json') as f:
    bounds = json.load(f)
    for key in bounds:
        year = key.split('/')[0].split('sp')[1]
        if year in bounds_by_year:
            bounds_by_year[year][key] = bounds[key]
        else:
            bounds_by_year[year] = {key: bounds[key]}

nbrss = {} 
fnamess = {}
for key in bounds_by_year:
    coords = []
    fnames = []
    for key2 in sorted(bounds_by_year[key]):
        coords.append([bounds_by_year[key][key2][0][0], bounds_by_year[key][key2][0][1]])
        fnames.append(key2)
    coords = np.array(coords)
    fnames = np.array(fnames)
    nbrs = NearestNeighbors(n_neighbors=4).fit(coords)
    nbrss[key] = nbrs
    fnamess[key] = fnames

dates = ["2016-01-01", "2018-01-01", "2020-01-01", "2022-01-01"]
years = ["16", "18", "20", "22"]
dates = np.array([np.datetime64(date) for date in dates])
print(dates)

# dates = []

data = {}
counter = 0
for i in tqdm(range(len(satellite_centers['PoIs']))):
    # print(satellite_centers['PoIs'][i])
    date = np.datetime64(satellite_centers['Dates'][i].split(' ')[0])
    key = years[np.argmin(np.abs(dates - date))]
    distances, indices = nbrss[key].kneighbors(np.array([satellite_centers['PoIs'][i][::-1]]))
    for index in indices[0]:
        fname = fnamess[key][index]
        polybounds = bounds_by_year[key][fname]
        if satellite_centers['PoIs'][i][1] > polybounds[1][0] and satellite_centers['PoIs'][i][1] < polybounds[0][0] and satellite_centers['PoIs'][i][0] > polybounds[0][1] and satellite_centers['PoIs'][i][0] < polybounds[2][1]:
            # interpolate
            tl = polybounds[0]
            bl = polybounds[1]
            tr = polybounds[2]
            br = polybounds[3]
            # print(satellite_centers['PoIs'][i][1])
            # print(tl, bl, tr, br)
            pixelyl = (satellite_centers['PoIs'][i][1]-bl[0])/(tl[0]-bl[0])
            pixelyr = (satellite_centers['PoIs'][i][1]-br[0])/(tr[0]-br[0])

            pixelxt = (satellite_centers['PoIs'][i][0]-tl[1])/(tr[1]-tl[1])
            pixelxb = (satellite_centers['PoIs'][i][0]-bl[1])/(br[1]-bl[1])
            # print(pixelyl, pixelyr, pixelxt, pixelxb)
            pixelx = pixelxt*(1-(pixelyl+pixelyl)/2) + pixelxb*(pixelyl+pixelyl)/2
            pixely = pixelyl*(1-(pixelxt+pixelxb)/2) + pixelyr*(pixelxt+pixelxb)/2
            # print(pixelx, pixely, fname)
            if fname in data:
                data[fname].append([i, pixelx, pixely])
            else:
                data[fname] = [[i, pixelx, pixely]]
            counter += 1
            break

# json dump
print(counter)
with open('coordinates.json', 'w') as f:
    json.dump(data, f, indent=4)