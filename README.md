# Overview
Source code for my michaelchen.app website. It transcribes stuff.

# Installation
I run this on Ubuntu server in DigitalOcean. 
1. Create a python virtual environment `python3 -m venv env .`
2. Activate it with `source bin/activate`
3. Do `pip install requirements.txt`


#How to use
You can run it manually with `streamlit run app.py`

Or you can run it in the background with `nohup streamlit run app.py --server.port 80 &` (port 80 is http)

You can also run it with `./run.sh` which will re-start the script if it gets killed due to Out-Of-Memory error or whatever.

If `./run.sh` doesn't work because of permission error, give it executable permission with `chmod +x run.sh`
