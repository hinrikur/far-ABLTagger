
DIR=$1
# FOLDER=$(basename $PATH)

./utils/Dropbox-Uploader/dropbox_uploader.sh delete far/$(basename $DIR)
./utils/Dropbox-Uploader/dropbox_uploader.sh upload $DIR far/
