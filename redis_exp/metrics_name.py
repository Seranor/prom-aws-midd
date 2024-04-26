from prometheus_client import Gauge

redis_network_bandwidth_inallowance_exceeded = Gauge('redis_network_bandwidth_inallowance_exceeded',
                                                     'Redis NetworkBandwidthInAllowanceExceeded', ['ElastiCache'])

redis_network_bandwidthOut_allowance_exceeded = Gauge('redis_network_bandwidthOut_allowance_exceeded',
                                                   'Redis NetworkBandwidthInAllowanceExceeded', ['ElastiCache'])

redis_network_conntrack_allowance_exceeded = Gauge('redis_network_conntrack_allowance_exceeded',
                                                'Redis NetworkBandwidthInAllowanceExceeded', ['ElastiCache'])

redis_network_packetsPerSecond_allowance_exceeded = Gauge('redis_network_packetsPerSecond_allowance_exceeded',
                                                       'Redis NetworkBandwidthInAllowanceExceeded', ['ElastiCache'])

'''
超出了入站网络带宽限额
NetworkBandwidthInAllowanceExceeded

超出了出站网络带宽限额
NetworkBandwidthOutAllowanceExceeded

超出了网络连接跟踪限额
NetworkConntrackAllowanceExceeded

超出了每秒网络数据包限额
NetworkPacketsPerSecondAllowanceExceeded
'''
