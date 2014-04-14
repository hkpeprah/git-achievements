#!/bin/bash

function generate_new_secret {
    # Generates a new secret key and appends it to the custom application
    # settings.  The new secret key is generated using the python generation
    # script.
    BASEPATH=`basename $0`
    DIRNAME=`dirname $0`
    SCRIPTPATH="$DIRNAME/$BASEPATH"
    SECRET_KEY=`python $DIRNAME/generate_secret_key.py`
    SETTINGS="$DIRNAME/../gitachievements/settings/custom.py"

    echo "Generated new secret key: $SECRET_KEY"
    echo "SECRET_KEY = \"$SECRET_KEY\"" >> $SETTINGS
    exit 0
}

generate_new_secret $0
