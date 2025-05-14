# Yelp Loader – CS412 Project

## Add the Data Folder

The Yelp dataset is too large to host on GitHub.

1. Download, unzip, and untar from [Yelp Open Dataset](https://business.yelp.com/data/resources/open-dataset/).
2. Create a `data/` folder inside your project directory:
3. Place the following JSON files into `yelp-loader/data/`:
- `business.json`
- `review.json`
- `tip.json`
- `user.json`

You can do this by running this within the `/Yelp JSON` folder, **but make sure your filepaths are correct**:
```bash
mv yelp_academic_dataset_business.json ~/412-project/yelp-loader/data/business.json
```
```bash
mv yelp_academic_dataset_user.json ~/412-project/yelp-loader/data/user.json
```
```bash
mv yelp_academic_dataset_review.json ~/412-project/yelp-loader/data/review.json
```
```bash
mv yelp_academic_dataset_tip.json ~/412-project/yelp-loader/data/tip.json
```

---

## Installations

Make sure Python 3 and pip are installed:

```bash
python3 --version
pip --version
```

##### if 3.12: (use your version)
```bash
apt install python3.12-venv
```

##### creates a managed python env:
**ensure you are in the project folder (412-project/yelp-loader) for below command:**
```bash
python3 -m venv venv
```

##### starts it
```bash
source venv/bin/activate
```

to leave: 
```bash
deactivate
```

##### install the python -> psql scripting tool
**only do this after last command**
```bash
pip install psycopg2-binary --break-system-packages
```

##  Database Initialization 
##### Create the psql database cluster and launch the server locally
```bash
export PATH=$PATH:/lib/postgresql/16/bin
```
```bash
export PGPORT=8888
```
```bash
export PGHOST=/tmp
```
```bash
initdb $HOME/dbProject
```
```bash
pg_ctl -D $HOME/dbProject -o '-k /tmp' start
```

## Set up and run the makefile
##### modify 412-Project/yelp-loader/populate_db.py
replace `USERNAME` with your system username (bash: whoami)
##### if JSON files properly added, below command will work (takes some time)
```
make full
```
