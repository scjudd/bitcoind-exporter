import logging
import os

from bitcoin_rpc_exporter import BitcoinRpcExporter
from json_rpc_client import JsonRpcClient
from prometheus_metrics import PrometheusMetrics

logging.basicConfig(
    format='%(actime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

endpoint = os.environ.get('BITCOIN_RPC_ENDPOINT', 'http://127.0.0.1:8332')
username = os.environ.get('BITCOIN_RPC_USERNAME', 'metrics')
password = os.environ['BITCOIN_RPC_PASSWORD']

rpc_client = JsonRpcClient(endpoint, username, password)
metrics = PrometheusMetrics(start_server=True)
exporter = BitcoinRpcExporter(rpc_client, metrics)

exporter.run()
