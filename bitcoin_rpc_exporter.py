import logging
import time

class BitcoinRpcExporter:
    def __init__(self, rpc_client, metrics):
        self.rpc_client = rpc_client
        self.metrics = metrics
        self.interval_seconds = 1

    def run_once(self):
        blockhash = self.rpc_client.call('getbestblockhash')
        block = self.rpc_client.call('getblock', [blockhash])
        self.metrics.best_block_index.set(block['height'])
        self.metrics.best_block_time.set(block['time'])

        difficulty = self.rpc_client.call('getdifficulty')
        self.metrics.chain_difficulty.set(difficulty)

        networkinfo = self.rpc_client.call('getnetworkinfo')
        self.metrics.peer_connections.set(networkinfo['connections'])

    def run(self):
        while True:
            try:
                self.run_once()
                if self.interval_seconds != 1:
                    self.interval_seconds = 1
                    logging.info('reset interval to one second')
            except Exception:
                self.interval_seconds = min(self.interval_seconds << 1, 32)
                logging.exception(
                    'json-rpc error occurred, set interval to {} seconds'.format(
                        self.interval_seconds))
            finally:
                time.sleep(self.interval_seconds)
