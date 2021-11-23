
# Eurekalabs_tp

Eurekalabs project

## Installation

To run this project Docker will be needed , use the following link https://www.docker.com/ \
Then Git clone https://github.com/PatricioHenderson/eurekalabs



## Getting Started

```python
docker-compose up

cd eurekalabs_tp
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```


## Runing
http://localhost:8000/admin where will be able to log in with the superuser.

http://localhost:8080 to check tables.

https://eurekalabstp.herokuapp.com/stock_market/user/login/ is a POST api where user should log in. Form data has to be in the body { 'username':'example' , 'last_name':'Example_last_name', 'email':'test@email.com'}.

http://localhost:8000/stock_market/stock_information/?simbol=FB is a GET api to get the stock information. Params = { 'simbol':'AAPL'} Headers{ Authorization: Token <token> } Note that the token has been generated during the login.
