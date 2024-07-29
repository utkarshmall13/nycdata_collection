### Setup

See `setup.sh` for mamba/conda environment.

After setup run `mkdir data` to create a data directory where outputs will be stored.

### Download flickr metadata first
Create a flickr account and obtain an api key using this [link](https://www.flickr.com/services/api/misc.api_keys.html).
Once you have the key, use it in the following script.

> cd src
> python3 get_flickr_metadata.py

In the script it is only done for NYC, you'll have to use your own shapefiles for custom dataset. This will create a directory named `metadata`

### After metadata download use `subsample_dedup_bin.py` to get unique image metadata

> python3 subsample_dedup_bin.py

This will create another directory named `metadata_sdb`.

### After deduplicating download the flickr images using this metadata.

> python3 get_images.py

This will create another directory named `images`.

### Not all images will be downloaded, use `filter_existing_and_rename.py` to only filter down metadata of valid images.

> python3 filter_existing_and_rename.py

### Once we have the final metadata and images, use `satellite_sampler.py` to obtain center points of satellite images to be sampled.

> python3 satellite_sampler.py

This will give two outputs one is the image data `satellite_centers.pkl` contain center points to be sampled. 
The second thing it contains is satellite center to ground images mapping `image_data.pkl`. If you can get these two pickle piles you can go to the next step of downloading naip images.

## Downloading ortho imagery

### Get raw ortho imagery

Use `download_ortho.py` to download the raw ortho iamgery from New York's GIS data website. 

### Processing ortho imagery
The ortho imagery are in format not suitable for deep learning applications. So we first convert it into computer vision format.

run the following three scripts:

> python3 convert_orthojp22jpg.py
This converts jp2 images to jpeg images. Then to get geocoordinate bounds of these images run `get_ortho_bounds.py`

> python3 get_ortho_bounds.py

After getting bounds for ortho images, use `get_cropped_image_coordinates.py` to get cropped image bounds for the corresponding ground images. 

> python3 get_cropped_image_coordinates.py

Finally, run

> python3 get_cropped_images.py

to obtain the cropeed images corresponding to ground images.

### Get pair of satellite and ground images.

Optionally run `create_train_test_split.py` to get pairs of satellite and ground images. This will create a directory `split_m2o` with csvs containing paired ground-satellite images.








