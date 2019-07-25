import prometheus_client as pc

class PrometheusMetrics:

    def __init__(self, start_server):
        if start_server:
            pc.start_http_server(8000)

        self.best_block_index = pc.Gauge(
            'bitcoind_best_block_index',
            'The block height or index')

        self.best_block_time = pc.Gauge(
            'bitcoind_best_block_timestamp_seconds',
            'The block time in seconds since epoch (Jan 1 1970 GMT)')

        self.chain_difficulty = pc.Gauge(
            'bitcoind_chain_difficulty',
            'The proof-of-work difficulty as a multiple of the minimum difficulty')

        self.peer_connections = pc.Gauge(
            'bitcoind_peer_connections',
            'The number of connected peers')
