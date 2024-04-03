from flask import Flask, Response, request
import grpc
from lnd_connection import connection_lnd,ln
import functools
from hashlib import sha256

""" 
In this vector the hashes of the invoices that are generated will be stored.
"""
invoice_hashes = []

app = Flask(__name__)

"""
    The payment hashes will be managed in a hexadecimal string for ease of manipulation
    Before applying sha256 the hexadecimal string must be converted to binary
"""
def hash_sha256(data_hex):
    data_bytes=bytes.fromhex(data_hex) 
    bytes_hashed= sha256(data_bytes).digest()
    return bytes_hashed.hex()

def verify_preimage(preimage):    
    preimage_hash = hash_sha256(preimage)
    print(f"preimage={preimage} hash={preimage_hash}")
    found = False
    for hash in invoice_hashes:
            if hash == preimage_hash:
                    found = True
    # pay-per-view means you pay every time.
    if found:
            invoice_hashes.remove(preimage_hash)
            
    return found

def verify_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
                # go get invoice!
                pass
        else:
                print(request.headers["Authorization"])
                parts = request.headers["Authorization"].split()
                if len(parts) == 2 and parts[0] == "L402":
                        rune, preimage = parts[1].split(':', maxsplit=1)
                        if verify_preimage(preimage):
                                return func(*args, **kwargs) 

        amount_sat=200
        comment="payment for endpoint L402"
        invoice_req = ln.Invoice(
        value=amount_sat,
        memo=comment
        )

        conn_lnd = connection_lnd("invoice")

        try:
            rs = conn_lnd.AddInvoice(invoice_req)                            
            bolt11 = rs.payment_request 
            # r_hash comes in bytes and we convert it to hexadecimal  
            invoice_hashes.append(rs.r_hash.hex())
                        
            resp = Response("Needs payment", status=402)
            resp.headers["WWW-Authenticate"] = 'L402 token="", invoice="{}"'.format(bolt11)
        except grpc.RpcError as e:
            print(f"Error: e_status={e.code()} message={e.details()} debug={e.debug_error_string()}")
            resp = Response("Bolt11 not generated", status=500)
        
        return resp
    return wrapper
        

@app.route('/')
@verify_auth
def index():
    return 'Premium content \n'

app.run(host='0.0.0.0', port=8080)