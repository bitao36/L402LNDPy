# Flask endpoint that implement the standar L402 

This repository contains a python flask server that use the standar L402
to return premium content

## Requirements

- Python 3.6 or higher
- Python dependencies `flask`,`decouple`,`grpcio`,`protobuf`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/bitao36/L402LNDPY.git
cd L402LNDPY
```

2. Create a virtual environment and activate it:

**For Linux:**

install these dependencies for use mysqlclient
```
sudo apt-get install python3-dev
```

Install virtual environment just the first time

```bash
python3 -m venv venv
```

Activate the virtual environment (activate the environment every time you go to run the endpoint)


```bash
source venv/bin/activate
```

**For Windows:**


Install virtual environment just the first time


```bash
virtualenv venv
```

Activate the virtual environment (activate the environment every time you go to run the endpoint)

```bash
venv\Scripts\.\activate
```


3. Install the required dependencies:

```bash
pip install -r requirements.txt
```


### Environment Variables

You must create a file .env and to add the following environment variables to customize the connection to the database:

```bash=
LND_RPC_ADDRESS=127.0.0.1:10001
LND_TLS_CERT_PATH=credentials/tls.cert
LND_INVOICE_MACAROON_PATH=credentials/invoices.macaroon
LND_ADMIN_MACAROON_PATH=credentials/admin.macaroon
```


## Access the application

```
python3 app.py
```

The webserver is listening on 8080 so you must go to one client and to do a request: 

GET http://localhost:8080

The server response is:

```
status_code: 402
Content    : "Needs payment"
```
Y en headers:

```
WWW-Authenticate= L402 token="",invoice=<bolt11>
```     

When you pay the bolt11 invoice and get preimage you must add next header to same request:

```
Authorization=L402 token:<preimage>
```

And now you can access premium content.