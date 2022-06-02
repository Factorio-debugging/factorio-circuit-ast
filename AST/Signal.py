from enum import Enum
from typing import List


class Signal(Enum):
    ROCKET_FUEL: str = "rocket-fuel"
    ADVANCED_CIRCUIT: str = "advanced-circuit"
    SULFURIC_ACID_BARREL: str = "sulfuric-acid-barrel"
    EXPLOSIVES: str = "explosives"
    IRON_ORE: str = "iron-ore"
    URANIUM_FUEL_CELL: str = "uranium-fuel-cell"
    WOODEN_CHEST: str = "wooden-chest"
    CONSTANT_COMBINATOR: str = "constant-combinator"
    LIGHT_OIL_BARREL: str = "light-oil-barrel"
    RED_WIRE: str = "red-wire"
    CONSTRUCTION_ROBOT: str = "construction-robot"
    STEAM_TURBINE: str = "steam-turbine"
    ASSEMBLING_MACHINE_3: str = "assembling-machine-3"
    EXOSKELETON_EQUIPMENT: str = "exoskeleton-equipment"
    LONG_HANDED_INSERTER: str = "long-handed-inserter"
    ROCKET_CONTROL_UNIT: str = "rocket-control-unit"
    FAST_TRANSPORT_BELT: str = "fast-transport-belt"
    COPPER_ORE: str = "copper-ore"
    RADAR: str = "radar"
    STEEL_CHEST: str = "steel-chest"
    FILTER_INSERTER: str = "filter-inserter"
    STEEL_FURNACE: str = "steel-furnace"
    SMALL_LAMP: str = "small-lamp"
    ENERGY_SHIELD_EQUIPMENT: str = "energy-shield-equipment"
    POWER_SWITCH: str = "power-switch"
    ASSEMBLING_MACHINE_1: str = "assembling-machine-1"
    ENGINE_UNIT: str = "engine-unit"
    FUSION_REACTOR_EQUIPMENT: str = "fusion-reactor-equipment"
    RAIL_CHAIN_SIGNAL: str = "rail-chain-signal"
    PROGRAMMABLE_SPEAKER: str = "programmable-speaker"
    IRON_PLATE: str = "iron-plate"
    HEAT_EXCHANGER: str = "heat-exchanger"
    CRUDE_OIL_BARREL: str = "crude-oil-barrel"
    MEDIUM_ELECTRIC_POLE: str = "medium-electric-pole"
    URANIUM_235: str = "uranium-235"
    URANIUM_238: str = "uranium-238"
    NUCLEAR_FUEL: str = "nuclear-fuel"
    LAB: str = "lab"
    TRAIN_STOP: str = "train-stop"
    RAIL_SIGNAL: str = "rail-signal"
    COPPER_PLATE: str = "copper-plate"
    OIL_REFINERY: str = "oil-refinery"
    SPLITTER: str = "splitter"
    SOLID_FUEL: str = "solid-fuel"
    LOGISTIC_CHEST_REQUESTER: str = "logistic-chest-requester"
    LOGISTIC_CHEST_PASSIVE_PROVIDER: str = "logistic-chest-passive-provider"
    FLAMETHROWER_TURRET: str = "flamethrower-turret"
    FAST_INSERTER: str = "fast-inserter"
    ELECTRIC_FURNACE: str = "electric-furnace"
    PUMP: str = "pump"
    ELECTRIC_MINING_DRILL: str = "electric-mining-drill"
    INSERTER: str = "inserter"
    IRON_GEAR_WHEEL: str = "iron-gear-wheel"
    PIPE: str = "pipe"
    BATTERY_MK2_EQUIPMENT: str = "battery-mk2-equipment"
    EXPRESS_SPLITTER: str = "express-splitter"
    EXPRESS_TRANSPORT_BELT: str = "express-transport-belt"
    IRON_STICK: str = "iron-stick"
    LANDFILL: str = "landfill"
    LOGISTIC_CHEST_ACTIVE_PROVIDER: str = "logistic-chest-active-provider"
    OFFSHORE_PUMP: str = "offshore-pump"
    ROCKET_SILO: str = "rocket-silo"
    FAST_UNDERGROUND_BELT: str = "fast-underground-belt"
    WOOD: str = "wood"
    LAND_MINE: str = "land-mine"
    BURNER_MINING_DRILL: str = "burner-mining-drill"
    STACK_FILTER_INSERTER: str = "stack-filter-inserter"
    ASSEMBLING_MACHINE_2: str = "assembling-machine-2"
    CONCRETE: str = "concrete"
    GREEN_WIRE: str = "green-wire"
    PIPE_TO_GROUND: str = "pipe-to-ground"
    NUCLEAR_REACTOR: str = "nuclear-reactor"
    STONE_BRICK: str = "stone-brick"
    SOLAR_PANEL_EQUIPMENT: str = "solar-panel-equipment"
    LOGISTIC_ROBOT: str = "logistic-robot"
    DECIDER_COMBINATOR: str = "decider-combinator"
    STEEL_PLATE: str = "steel-plate"
    FLYING_ROBOT_FRAME: str = "flying-robot-frame"
    BEACON: str = "beacon"
    HEAVY_OIL_BARREL: str = "heavy-oil-barrel"
    LUBRICANT_BARREL: str = "lubricant-barrel"
    PROCESSING_UNIT: str = "processing-unit"
    PETROLEUM_GAS_BARREL: str = "petroleum-gas-barrel"
    TRANSPORT_BELT: str = "transport-belt"
    WATER_BARREL: str = "water-barrel"
    ARITHMETIC_COMBINATOR: str = "arithmetic-combinator"
    UNDERGROUND_BELT: str = "underground-belt"
    ELECTRONIC_CIRCUIT: str = "electronic-circuit"
    ARTILLERY_TURRET: str = "artillery-turret"
    EMPTY_BARREL: str = "empty-barrel"
    LASER_TURRET: str = "laser-turret"
    PERSONAL_ROBOPORT_EQUIPMENT: str = "personal-roboport-equipment"
    DISCHARGE_DEFENSE_EQUIPMENT: str = "discharge-defense-equipment"
    PERSONAL_LASER_DEFENSE_EQUIPMENT: str = "personal-laser-defense-equipment"
    ENERGY_SHIELD_MK2_EQUIPMENT: str = "energy-shield-mk2-equipment"
    NIGHT_VISION_EQUIPMENT: str = "night-vision-equipment"
    PERSONAL_ROBOPORT_MK2_EQUIPMENT: str = "personal-roboport-mk2-equipment"
    GUN_TURRET: str = "gun-turret"
    LOW_DENSITY_STRUCTURE: str = "low-density-structure"
    REFINED_HAZARD_CONCRETE: str = "refined-hazard-concrete"
    COAL: str = "coal"
    STORAGE_TANK: str = "storage-tank"
    BIG_ELECTRIC_POLE: str = "big-electric-pole"
    COPPER_CABLE: str = "copper-cable"
    CHEMICAL_PLANT: str = "chemical-plant"
    ELECTRIC_ENGINE_UNIT: str = "electric-engine-unit"
    STACK_INSERTER: str = "stack-inserter"
    STONE_WALL: str = "stone-wall"
    BATTERY_EQUIPMENT: str = "battery-equipment"
    STONE: str = "stone"
    BURNER_INSERTER: str = "burner-inserter"
    SOLAR_PANEL: str = "solar-panel"
    BELT_IMMUNITY_EQUIPMENT: str = "belt-immunity-equipment"
    BOILER: str = "boiler"
    STEAM_ENGINE: str = "steam-engine"
    HAZARD_CONCRETE: str = "hazard-concrete"
    HEAT_PIPE: str = "heat-pipe"
    GATE: str = "gate"
    LOGISTIC_CHEST_STORAGE: str = "logistic-chest-storage"
    ACCUMULATOR: str = "accumulator"
    STONE_FURNACE: str = "stone-furnace"
    LOGISTIC_CHEST_BUFFER: str = "logistic-chest-buffer"
    SMALL_ELECTRIC_POLE: str = "small-electric-pole"
    EXPRESS_UNDERGROUND_BELT: str = "express-underground-belt"
    ROBOPORT: str = "roboport"
    PUMPJACK: str = "pumpjack"
    SULFUR: str = "sulfur"
    PLASTIC_BAR: str = "plastic-bar"
    REFINED_CONCRETE: str = "refined-concrete"
    FAST_SPLITTER: str = "fast-splitter"
    SUBSTATION: str = "substation"
    CENTRIFUGE: str = "centrifuge"
    BATTERY: str = "battery"
    SATELLITE: str = "satellite"
    URANIUM_ORE: str = "uranium-ore"
    IRON_CHEST: str = "iron-chest"
    USED_UP_URANIUM_FUEL_CELL: str = "used-up-uranium-fuel-cell"
    TANK: str = "tank"
    SPIDERTRON: str = "spidertron"
    LOCOMOTIVE: str = "locomotive"
    CARGO_WAGON: str = "cargo-wagon"
    ARTILLERY_WAGON: str = "artillery-wagon"
    FLUID_WAGON: str = "fluid-wagon"
    CAR: str = "car"
    UTILITY_SCIENCE_PACK: str = "utility-science-pack"
    AUTOMATION_SCIENCE_PACK: str = "automation-science-pack"
    MILITARY_SCIENCE_PACK: str = "military-science-pack"
    LOGISTIC_SCIENCE_PACK: str = "logistic-science-pack"
    SPACE_SCIENCE_PACK: str = "space-science-pack"
    CHEMICAL_SCIENCE_PACK: str = "chemical-science-pack"
    PRODUCTION_SCIENCE_PACK: str = "production-science-pack"
    CANNON_SHELL: str = "cannon-shell"
    EXPLOSIVE_URANIUM_CANNON_SHELL: str = "explosive-uranium-cannon-shell"
    PIERCING_ROUNDS_MAGAZINE: str = "piercing-rounds-magazine"
    FLAMETHROWER_AMMO: str = "flamethrower-ammo"
    PIERCING_SHOTGUN_SHELL: str = "piercing-shotgun-shell"
    ROCKET: str = "rocket"
    URANIUM_CANNON_SHELL: str = "uranium-cannon-shell"
    SHOTGUN_SHELL: str = "shotgun-shell"
    EXPLOSIVE_ROCKET: str = "explosive-rocket"
    EXPLOSIVE_CANNON_SHELL: str = "explosive-cannon-shell"
    ARTILLERY_SHELL: str = "artillery-shell"
    ATOMIC_BOMB: str = "atomic-bomb"
    URANIUM_ROUNDS_MAGAZINE: str = "uranium-rounds-magazine"
    FIREARM_MAGAZINE: str = "firearm-magazine"
    EFFECTIVITY_MODULE_2: str = "effectivity-module-2"
    EFFECTIVITY_MODULE_3: str = "effectivity-module-3"
    SPEED_MODULE: str = "speed-module"
    PRODUCTIVITY_MODULE: str = "productivity-module"
    PRODUCTIVITY_MODULE_2: str = "productivity-module-2"
    EFFECTIVITY_MODULE: str = "effectivity-module"
    SPEED_MODULE_2: str = "speed-module-2"
    SPEED_MODULE_3: str = "speed-module-3"
    PRODUCTIVITY_MODULE_3: str = "productivity-module-3"
    POWER_ARMOR: str = "power-armor"
    MODULAR_ARMOR: str = "modular-armor"
    HEAVY_ARMOR: str = "heavy-armor"
    POWER_ARMOR_MK2: str = "power-armor-mk2"
    LIGHT_ARMOR: str = "light-armor"
    COMBAT_SHOTGUN: str = "combat-shotgun"
    PISTOL: str = "pistol"
    ROCKET_LAUNCHER: str = "rocket-launcher"
    SUBMACHINE_GUN: str = "submachine-gun"
    SHOTGUN: str = "shotgun"
    FLAMETHROWER: str = "flamethrower"
    CLIFF_EXPLOSIVES: str = "cliff-explosives"
    DEFENDER_CAPSULE: str = "defender-capsule"
    DISCHARGE_DEFENSE_REMOTE: str = "discharge-defense-remote"
    GRENADE: str = "grenade"
    DESTROYER_CAPSULE: str = "destroyer-capsule"
    SLOWDOWN_CAPSULE: str = "slowdown-capsule"
    ARTILLERY_TARGETING_REMOTE: str = "artillery-targeting-remote"
    DISTRACTOR_CAPSULE: str = "distractor-capsule"
    RAW_FISH: str = "raw-fish"
    POISON_CAPSULE: str = "poison-capsule"
    CLUSTER_GRENADE: str = "cluster-grenade"
    BLUEPRINT: str = "blueprint"
    BLUEPRINT_BOOK: str = "blueprint-book"
    UPGRADE_PLANNER: str = "upgrade-planner"
    DECONSTRUCTION_PLANNER: str = "deconstruction-planner"
    SPIDERTRON_REMOTE: str = "spidertron-remote"
    REPAIR_PACK: str = "repair-pack"
    RAIL: str = "rail"
    LIGHT_OIL: str = "light-oil"
    SULFURIC_ACID: str = "sulfuric-acid"
    WATER: str = "water"
    PETROLEUM_GAS: str = "petroleum-gas"
    CRUDE_OIL: str = "crude-oil"
    STEAM: str = "steam"
    LUBRICANT: str = "lubricant"
    HEAVY_OIL: str = "heavy-oil"
    SIGNAL_INFO: str = "signal-info"
    SIGNAL_DOT: str = "signal-dot"
    SIGNAL_GREY: str = "signal-grey"
    SIGNAL_5: str = "signal-5"
    SIGNAL_3: str = "signal-3"
    SIGNAL_K: str = "signal-K"
    SIGNAL_W: str = "signal-W"
    SIGNAL_YELLOW: str = "signal-yellow"
    SIGNAL_GREEN: str = "signal-green"
    SIGNAL_0: str = "signal-0"
    SIGNAL_D: str = "signal-D"
    SIGNAL_Q: str = "signal-Q"
    SIGNAL_A: str = "signal-A"
    SIGNAL_1: str = "signal-1"
    SIGNAL_4: str = "signal-4"
    SIGNAL_8: str = "signal-8"
    SIGNAL_Z: str = "signal-Z"
    SIGNAL_6: str = "signal-6"
    SIGNAL_Y: str = "signal-Y"
    SIGNAL_I: str = "signal-I"
    SIGNAL_2: str = "signal-2"
    SIGNAL_B: str = "signal-B"
    SIGNAL_X: str = "signal-X"
    SIGNAL_V: str = "signal-V"
    SIGNAL_S: str = "signal-S"
    SIGNAL_R: str = "signal-R"
    SIGNAL_G: str = "signal-G"
    SIGNAL_BLUE: str = "signal-blue"
    SIGNAL_N: str = "signal-N"
    SIGNAL_P: str = "signal-P"
    SIGNAL_T: str = "signal-T"
    SIGNAL_O: str = "signal-O"
    SIGNAL_U: str = "signal-U"
    SIGNAL_F: str = "signal-F"
    SIGNAL_M: str = "signal-M"
    SIGNAL_7: str = "signal-7"
    SIGNAL_CYAN: str = "signal-cyan"
    SIGNAL_L: str = "signal-L"
    SIGNAL_J: str = "signal-J"
    SIGNAL_H: str = "signal-H"
    SIGNAL_WHITE: str = "signal-white"
    SIGNAL_CHECK: str = "signal-check"
    SIGNAL_BLACK: str = "signal-black"
    SIGNAL_9: str = "signal-9"
    SIGNAL_PINK: str = "signal-pink"
    SIGNAL_RED: str = "signal-red"
    SIGNAL_C: str = "signal-C"
    SIGNAL_E: str = "signal-E"
    SIGNAL_EVERYTHING: str = "signal-everything"
    SIGNAL_ANYTHING: str = "signal-anything"
    SIGNAL_EACH: str = "signal-each"


AbstractSignal: List[Signal] = [
    Signal.SIGNAL_EVERYTHING,
    Signal.SIGNAL_ANYTHING,
    Signal.SIGNAL_EACH,
]

ConcreteSignal: List[Signal] = [
    signal for signal in Signal.__members__.values() if signal not in AbstractSignal
]
