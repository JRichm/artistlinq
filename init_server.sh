sudo apt update
sudo apt update

pip install -r requirements.txt
export PATH=$PATH:/usr/local/python3/bin && pip install gunicorn && gunicorn server:app

cat requirements.txt
