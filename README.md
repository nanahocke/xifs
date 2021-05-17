# xifs
# Installation
install dependencies
```
curl -X GET "https://raw.githubusercontent.com/nanahocke/xifs/main/environment.yml" -o xifs_environment.yml
conda env create -n xifs_env -f xifs_environment.yml
```
Install xifs
```
conda activate xifs_env
pip install git+https://github.com/nanahocke/xifs.git@main
```
