from typing import List, TypedDict, Optional, Dict, Tuple
from weakref import ReferenceType

from draftsman.classes.mixins import CircuitConnectableMixin


class BaseEntityReference(TypedDict):
    entity_id: ReferenceType[CircuitConnectableMixin]


class EntityReference(BaseEntityReference, total=False):
    circuit_id: int


ConnectedEntities = List[EntityReference]

Connections = Dict[str, Dict[str, ConnectedEntities]]


def get_all_connections(
    src: CircuitConnectableMixin, color: str, side: Optional[str] = None
) -> List[Tuple[CircuitConnectableMixin, int]]:
    assert color in ("red", "green")
    side = side or "1"
    assert side in ("1", "2")
    net_side: Dict[str, ConnectedEntities]
    conn: ConnectedEntities
    if (net_side := src.connections.get(side)) and (conn := net_side.get(color)):
        return [(i["entity_id"](), i.get("circuit_id", 1)) for i in conn]
    return []
