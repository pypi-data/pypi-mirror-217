# coding=utf8
## Copyright (c) 2020 Arseniy Kuznetsov
##
## This program is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License
## as published by the Free Software Foundation; either version 2
## of the License, or (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.


from collections import namedtuple
from mktxp.cli.config.config import config_handler, MKTXPConfigKeys, CollectorKeys
from mktxp.flow.router_connection import RouterAPIConnection


class RouterEntry:
    ''' RouterOS Entry
    '''                 
    def __init__(self, router_name):
        self.router_name = router_name
        self.config_entry  = config_handler.config_entry(router_name)
        self.api_connection = RouterAPIConnection(router_name, self.config_entry)
        self.router_id = {
            MKTXPConfigKeys.ROUTERBOARD_NAME: self.router_name,
            MKTXPConfigKeys.ROUTERBOARD_ADDRESS: self.config_entry.hostname
            }
        
        self.wifi_package = None
        self.time_spent =  { CollectorKeys.IDENTITY_COLLECTOR: 0,
                            CollectorKeys.SYSTEM_RESOURCE_COLLECTOR: 0,
                            CollectorKeys.HEALTH_COLLECTOR: 0,
                            CollectorKeys.PUBLIC_IP_ADDRESS_COLLECTOR: 0,
                            CollectorKeys.IPV6_NEIGHBOR_COLLECTOR: 0,
                            CollectorKeys.PACKAGE_COLLECTOR: 0,
                            CollectorKeys.DHCP_COLLECTOR: 0,
                            CollectorKeys.POOL_COLLECTOR: 0,
                            CollectorKeys.IP_CONNECTION_COLLECTOR: 0,
                            CollectorKeys.INTERFACE_COLLECTOR: 0,
                            CollectorKeys.FIREWALL_COLLECTOR: 0,
                            CollectorKeys.MONITOR_COLLECTOR: 0,
                            CollectorKeys.POE_COLLECTOR: 0,
                            CollectorKeys.NETWATCH_COLLECTOR: 0,
                            CollectorKeys.ROUTE_COLLECTOR: 0,
                            CollectorKeys.WLAN_COLLECTOR: 0,
                            CollectorKeys.CAPSMAN_COLLECTOR: 0,
                            CollectorKeys.QUEUE_TREE_COLLECTOR: 0,
                            CollectorKeys.QUEUE_SIMPLE_COLLECTOR: 0,                            
                            CollectorKeys.USER_COLLECTOR: 0,                            
                            CollectorKeys.MKTXP_COLLECTOR: 0
                            }         
        self._dhcp_entry = None
        self._dhcp_records = {}
                                    
    @property
    def dhcp_entry(self):
        if self._dhcp_entry:
            return self._dhcp_entry
        return self
    @dhcp_entry.setter
    def dhcp_entry(self, dhcp_entry):
        self._dhcp_entry = dhcp_entry

    @property
    def dhcp_records(self):
        return (entry.record for key, entry in  self._dhcp_records.items() if entry.type == 'mac_address') \
                                                                                if self._dhcp_records else None   
    @dhcp_records.setter
    def dhcp_records(self, dhcp_records):
        for dhcp_record in dhcp_records:
            if dhcp_record.get('mac_address'):
                self._dhcp_records[dhcp_record.get('mac_address')] = DHCPCacheEntry('mac_address', dhcp_record)
            if dhcp_record.get('address'):
                dhcp_record['type'] = 'address'
                self._dhcp_records[dhcp_record.get('address')] = DHCPCacheEntry('address', dhcp_record)

    def dhcp_record(self, key):
        if self._dhcp_records and self._dhcp_records.get(key):
            return self._dhcp_records[key].record
        return None

    def is_ready(self):
        self.is_done() #flush caches, just in case
        is_ready = True
        if not self.api_connection.is_connected():
            is_ready = False                        
            # let's get connected now
            self.api_connection.connect()
            if self._dhcp_entry:
                self._dhcp_entry.api_connection.connect()
        return is_ready

    def is_done(self):
        self.wifi_package = None 
        self._dhcp_records = {}

DHCPCacheEntry = namedtuple('DHCPCacheEntry', ['type', 'record'])
