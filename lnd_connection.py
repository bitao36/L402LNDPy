import grpc, os, binascii
from decouple import config
from lnd_protos import lightning_pb2 as ln, lightning_pb2_grpc as lnrpc

def read_macaroon(macaroon_path):
    with open(macaroon_path, 'rb') as f:
        macaroon_bytes = f.read()
    return binascii.hexlify(macaroon_bytes).decode('utf-8')

def connection_lnd(type_macaroon):    

    lnd_rpc_address=config('LND_RPC_ADDRESS')
    tls_cert_path =config('LND_TLS_CERT_PATH')
    macaroon_path =config('LND_ADMIN_MACAROON_PATH')
    if type_macaroon=="invoice":
        macaroon_path =config('LND_INVOICE_MACAROON_PATH')

    with open(tls_cert_path, 'rb') as f:
        tls_cert = f.read()

    macaroon = read_macaroon(macaroon_path)
    creds = grpc.ssl_channel_credentials(root_certificates=tls_cert)
    metadata = [('macaroon', macaroon)]
    metadata_plugin = grpc.metadata_call_credentials(lambda _, cb: cb(metadata, None))
    auth_creds = grpc.composite_channel_credentials(creds, metadata_plugin)
    auth_channel = grpc.secure_channel(lnd_rpc_address, auth_creds)
    auth_stub = lnrpc.LightningStub(auth_channel)
    return auth_stub
