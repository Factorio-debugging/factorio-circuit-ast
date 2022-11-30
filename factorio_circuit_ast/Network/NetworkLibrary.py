from typing import Dict, Optional

from .Network import Network, NetworkType


class NetworkLibrary:
    def __init__(self) -> None:
        self.networks: Dict[int, Network] = {}

    def __contains__(self, item: Network) -> bool:
        return item in self.networks.values()

    def add_network(
        self, network_type: NetworkType, nid: Optional[int] = None
    ) -> Network:
        nid = nid if nid is not None else max([*self.networks.keys(), 0]) + 1
        net: Network = Network(nid, network_type)
        self.networks[nid] = net
        return net

    def __getitem__(self, item: int) -> Network:
        return self.networks[item]

    def get_or_create_network(self, nid: int, network_type: NetworkType) -> Network:
        if nid in self.networks:
            assert (
                net := self.networks[nid]
            ).type == network_type, "The stored network has the wrong type"
            return net
        return self.add_network(network_type, nid)
