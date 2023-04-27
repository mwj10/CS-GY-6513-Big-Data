#! /usr/bin/batch

export CURRENTDIR=$(pwd)
echo $CURRENTDIR

docker compose up -d

osascript -ss - "CURRENTDIR"<<EOF

    tell app "Terminal" 
    do script "
    cd $CURRENTDIR/news/extract &&
    source venv/bin/activate &&
    python app.py"
    activate
    end tell

    tell app "Terminal" 
    do script "
    cd $CURRENTDIR/news/sentiment-analysis &&
    source venv/bin/activate &&
    python app.py"
    activate
    end tell

    tell app "Terminal" 
    do script "
    cd $CURRENTDIR/lstm &&
    source venv/bin/activate &&
    python main.py"
    activate
    end tell

EOF

echo 'Three new terminal window have been opened.'
echo 'Please wait until they finished all processes.'