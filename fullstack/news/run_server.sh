#! /usr/bin/batch

export CURRENTDIR=$(pwd)
echo $CURRENTDIR

docker compose up -d

osascript -ss - "CURRENTDIR"<<EOF

    tell app "Terminal" 
    do script "
    cd $CURRENTDIR/extract &&
    source venv/bin/activate &&
    python app.py"
    activate
    end tell

    tell app "Terminal" 
    do script "
    cd $CURRENTDIR/sentiment-analysis &&
    source venv/bin/activate &&
    python app.py"
    activate
    end tell

EOF

echo 'Two new terminal window have been opened.'
echo 'Please wait until they finished all processes.'