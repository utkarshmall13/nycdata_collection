mamba create -n data_collection python=3.11 -y
mamba activate data_collection
pip install requests numpy fiona shapely matplotlib tqdm pillow scikit-learn earthengine-api wget
mamba install -c conda-forge gdal=3.9.0 -y
mamba install -c conda-forge libgdal-jp2openjpeg -y

mkdir data