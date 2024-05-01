#!/bin/bash
# starts the traffic app and restarts it if crashed

while true; do
    [ -e stopme ] && break
    streamlit run app.py --server.port 80
done
