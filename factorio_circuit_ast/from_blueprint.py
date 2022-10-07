from draftsman.prototypes.arithmetic_combinator import ArithmeticCombinator
from draftsman.prototypes.decider_combinator import DeciderCombinator
from draftsman.prototypes.constant_combinator import ConstantCombinator
from draftsman.classes.mixins import CircuitConnectableMixin
from typing import List, TypedDict, Optional, Dict
from weakref import ReferenceType
from .Network import Network, get_or_create_network, NetworkType


class BaseEntityReference(TypedDict):
    entity_id: ReferenceType[CircuitConnectableMixin]


class EntityReference(BaseEntityReference, total=False):
    circuit_id: int


ConnectedEntities = List[EntityReference]


Connections = Dict[str, Dict[str, ConnectedEntities]]


def get_network_for_entity(
    source: CircuitConnectableMixin, color: str, side: int = 1
) -> Optional[Network]:
    assert color in ("red", "green")
    str_side: str = str(side)
    circuit_id: Optional[int] = None
    observed: List[CircuitConnectableMixin] = [source]
    to_observe: List[CircuitConnectableMixin] = [source]
    while to_observe:
        current: CircuitConnectableMixin = to_observe.pop()
        if current in observed:
            continue
        if (
            current.connections
            and current.connections[str_side]
            and (conn := current.connections[str_side][color])
        ):
            for conn in conn:
                if "circuit_id" in conn:
                    circuit_id = conn['circuit_id']
                    break
                if entity := conn['entity_id']():
                    to_observe.append(entity)
    return get_or_create_network(sources[0]["circuit_id"], NetworkType(color))
