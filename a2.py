import math
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import Callable, Optional

from support import *

# Implement the classes, methods & functions described in the task sheet here


'''4.1.1 Weapon()'''
class Weapon:
    """
    Represents an abstract weapon class that provides basic properties and behaviors
    for all weapons in the game. Specific weapons should inherit from this class and
    override relevant attributes.
    """

    def __init__(self):
        self._name = "AbstractWeapon"  # Name of the weapon
        self._symbol = WEAPON_SYMBOL  # Symbol used to represent the weapon
        self._effect = {}  # Dictionary of effects the weapon can apply
        self._range = 0  # The range of the weapon's effect

    def get_name(self) -> str:
        """
        Returns the name of the weapon.
        """
        return self._name

    def get_symbol(self) -> str:
        """
        Returns the symbol that represents the weapon.
        """
        return self._symbol

    def get_effect(self) -> dict[str, int]:
        """
        Returns a dictionary containing the effects of the weapon.
        For example, {'poison': 2} would mean the weapon applies poison damage.
        """
        return self._effect

    def get_targets(self, position: Position) -> list[Position]:
        """
        Returns a list of positions that the weapon can target based on its range.
        The weapon will affect tiles in the same row and column within its range.

        Args:
            position (Position): The position from which the weapon is used.

        Returns:
            list[Position]: A list of positions that the weapon can target.
        """
        targets = []

        row, column = position

        # Add all target positions within the weapon's range
        for i in range(1, self._range + 1):
            targets.append((row + i, column))
            targets.append((row - i, column))
            targets.append((row, column + i))
            targets.append((row, column - i))
        return targets

    def __str__(self):
        """
        Returns the string representation of the weapon.
        """
        return self._name

    def __repr__(self):
        """
        Returns a representation of the weapon, primarily for debugging.
        """
        return "Weapon()"


#4.1.2 PoisonDart(Weapon)
class PoisonDart(Weapon):
    """
    Represents a specific type of weapon called PoisonDart.
    This weapon applies poison damage to its target.
    """

    def __init__(self):
        super().__init__()
        self._name = 'PoisonDart'  # Name of the weapon
        self._symbol = POISON_DART_SYMBOL  # Symbol of PoisonDart
        self._effect = {'poison': 2}  # Effect of the PoisonDart
        self._range = 2  # The range of the PoisonDart

    def __repr__(self):
        """
        Returns a string representation of the PoisonDart instance.
        """
        return "PoisonDart()"


#4.1.3 PoisonSword(Weapon)
class PoisonSword(Weapon):
    """
    Represents a specific type of weapon called PoisonSword.
    This weapon applies both regular damage and poison damage to its target.
    """

    def __init__(self):
        super().__init__()
        self._name = 'PoisonSword'  # Name of the weapon
        self._symbol = POISON_SWORD_SYMBOL  # Symbol of the PoisonSword
        self._effect = {'damage': 2, 'poison': 1}  # Effect of the PoisonSword
        self._range = 1  # The range of the PoisonSword

    def __repr__(self):
        """
        Returns a string representation of the PoisonSword instance.
        """
        return "PoisonSword()"


'''4.1.4 HealingRock(Weapon)'''

class HealingRock(Weapon):
    """
    Represents a specific type of weapon called HealingRock.
    This weapon heals its target when used.
    """
    def __init__(self):
        super().__init__()
        self._name = 'HealingRock'  # Name of the weapon
        self._symbol = HEALING_ROCK_SYMBOL  # Symbol of HealingRock
        self._effect = {'healing': 2}  # Effect of the HealingRock
        self._range = 2  # The range of the HealingRock

    def __repr__(self):
        """
        Returns a string representation of the HealingRock instance.
        """
        return "HealingRock()"


# 4.1.5 Tile()
class Tile:
    """
    Represents a tile in the dungeon map. A tile can either be blocking or non-blocking,
    and can optionally hold a weapon. Tiles are used to build the dungeon environment.
    """
    def __init__(self, symbol: str, is_blocking: bool) -> None:
        """
        Initializes a Tile with a symbol and blocking property.

        Args:
            symbol (str): The symbol that represents the tile (e.g., "#", " ", "G").
            is_blocking (bool): Determines if the tile blocks movement.
        """
        self._symbol = symbol  # Symbol of the tile
        self._is_blocking = is_blocking  # Whether the tile is blocking
        self._weapon = None  # Weapon on the tile (if any)

    def is_blocking(self) -> bool:
        """
        Returns whether the tile is blocking movement.

        Returns:
            bool: True if the tile is blocking, False otherwise.
        """
        return self._is_blocking

    def get_weapon(self) -> Optional[Weapon]:
        """
        Returns the weapon placed on the tile (if any).

        Returns:
            Optional[Weapon]: The weapon on the tile, or None if no weapon is present.
        """
        return self._weapon

    def set_weapon(self, weapon: Weapon) -> None:
        """
        Sets a weapon on the tile.

        Args:
            weapon (Weapon): The weapon to place on the tile.
        """
        self._weapon = weapon

    def remove_weapon(self) -> None:
        """
        Removes the weapon from the tile.
        """
        self._weapon = None

    def get_symbol(self) -> str:
        """
        Returns the symbol representing the tile.

        Returns:
            str: The symbol of the tile.
        """
        return self._symbol

    def __str__(self) -> str:
        """
        Returns the string representation of the tile.
        """
        return self._symbol

    def __repr__(self) -> str:
        """
        Returns a detailed representation of the tile, primarily for debugging.

        Returns:
            str: A string representation including the symbol and blocking status.
        """
        return f"Tile('{self._symbol}', {self._is_blocking})"


# 4.1.6 create_tile(symbol: str) -> Tile
def create_tile(symbol: str) -> Tile:
    """
    Creates a Tile object based on the given symbol.

    Each symbol corresponds to a specific type of tile in the dungeon:
    - "#" represents a wall (blocking tile).
    - " " represents a floor (non-blocking tile).
    - "G" represents a goal (non-blocking tile).
    - "D", "S", "H" represent tiles with corresponding weapons.

    Args:
        symbol (str): A character that represents the type of tile to create.

    Returns:
        Tile: A new Tile object corresponding to the symbol.
    """
    if symbol == WALL_TILE:
        return Tile(WALL_TILE, True)  # Blocking tile representing a wall
    elif symbol == GOAL_TILE:
        return Tile(GOAL_TILE, False)  # Non-blocking tile representing a goal
    elif symbol == PLAYER_SYMBOL:
        return Tile(FLOOR_TILE, False)  # Non-blocking tile for player start position
    elif symbol in [NICE_SLUG_SYMBOL, ANGRY_SLUG_SYMBOL, SCARED_SLUG_SYMBOL]:
        return Tile(FLOOR_TILE, False)  # Non-blocking tile for slug positions
    elif symbol in [POISON_DART_SYMBOL, POISON_SWORD_SYMBOL, HEALING_ROCK_SYMBOL]:
        tile = Tile(FLOOR_TILE, False)  # Non-blocking tile with a weapon
        if symbol == POISON_DART_SYMBOL:
            tile.set_weapon(PoisonDart())
        elif symbol == POISON_SWORD_SYMBOL:
            tile.set_weapon(PoisonSword())
        elif symbol == HEALING_ROCK_SYMBOL:
            tile.set_weapon(HealingRock())
        return tile
    else:
        return Tile(FLOOR_TILE, False)  # Default to non-blocking floor tile


#4.1.7 Entity()
class Entity:
    """
    Represents a basic entity in the game. Entities can have health,
    be affected by poison, and carry weapons. This class serves as a
    base for other specific entities like players and slugs.
    """

    def __init__(self, max_health: int) -> None:
        """
        Initializes an entity with a specified maximum health.

        Args:
            max_health (int): The maximum health the entity can have.
        """
        self._max_health = max_health  # Maximum health of the entity
        self._health = max_health  # Current health of the entity
        self._poison = 0  # Poison level affecting the entity
        self._weapon = None  # Weapon currently equipped by the entity

    def get_symbol(self) -> str:
        """
        Returns the symbol representing the entity.

        Returns:
            str: The symbol of the entity.
        """
        return ENTITY_SYMBOL

    def get_name(self) -> str:
        """
        Returns the name of the entity.

        Returns:
            str: The name of the entity.
        """
        return "Entity"

    def get_health(self) -> int:
        """
        Returns the current health of the entity.

        Returns:
            int: The current health value.
        """
        return self._health

    def get_poison(self) -> int:
        """
        Returns the current poison level of the entity.

        Returns:
            int: The poison level affecting the entity.
        """
        return self._poison

    def get_weapon(self) -> Optional[Weapon]:
        """
        Returns the weapon currently equipped by the entity.

        Returns:
            Optional[Weapon]: The equipped weapon or None if no weapon is equipped.
        """
        return self._weapon

    def equip(self, weapon: Weapon) -> None:
        """
        Equips a weapon to the entity.

        Args:
            weapon (Weapon): The weapon to equip.
        """
        self._weapon = weapon

    def get_weapon_targets(self, position: Position) -> list[Position]:
        """
        Returns a list of target positions based on the entity's equipped weapon.

        Args:
            position (Position): The current position of the entity.

        Returns:
            list[Position]: A list of positions that the weapon can target.
        """
        if self._weapon:
            return self._weapon.get_targets(position)
        return []

    def get_weapon_effect(self) -> dict[str, int]:
        """
        Returns the effects of the equipped weapon, if any.

        Returns:
            dict[str, int]: A dictionary of the weapon's effects.
        """
        if self._weapon:
            return self._weapon.get_effect()
        return {}

    def apply_effects(self, effects: dict[str, int]) -> None:
        """
        Applies a set of effects to the entity. Effects can include damage, healing, or poison.

        Args:
            effects (dict[str, int]): A dictionary of effects to apply (e.g., {'damage': 2, 'poison': 1}).
        """
        if 'damage' in effects:
            self._health = max(0, self._health - effects['damage'])
        if 'healing' in effects:
            self._health = min(self._max_health, self._health + effects['healing'])
        if 'poison' in effects:
            self._poison += effects['poison']

    def apply_poison(self) -> None:
        """
        Applies poison damage to the entity based on its current poison level.
        The poison level decreases by 1 after each application.
        """
        if self._poison > 0:
            self._health = max(0, self._health - self._poison)
            self._poison = max(0, self._poison - 1)

    def is_alive(self) -> bool:
        """
        Checks if the entity is still alive (health > 0).

        Returns:
            bool: True if the entity is alive, False otherwise.
        """
        return self.get_health() > 0

    def __str__(self) -> str:
        """
        Returns the string representation of the entity, showing its name.

        Returns:
            str: The name of the entity.
        """
        return self.get_name()

    def __repr__(self) -> str:
        """
        Returns a detailed representation of the entity, primarily for debugging.

        Returns:
            str: A string showing the entity type and its maximum health.
        """
        return f"Entity({self._max_health})"


#4.1.8 Player(Entity)
class Player(Entity):
    """
    Represents the player character in the game. The player can be affected
    by health, poison, and can equip weapons.
    """

    def __init__(self, max_health: int):
        """
        Initializes the player with a specified maximum health.

        Args:
            max_health (int): The maximum health of the player.
        """
        super().__init__(max_health)

    def get_symbol(self) -> str:
        """
        Returns the symbol that represents the player.

        Returns:
            str: The player's symbol.
        """
        return PLAYER_SYMBOL

    def get_name(self) -> str:
        """
        Returns the name of the player.

        Returns:
            str: The name "Player".
        """
        return "Player"

    def get_poison_level(self) -> int:
        """
        Returns the current poison level affecting the player.

        Returns:
            int: The player's poison level.
        """
        return self.get_poison()

    def __repr__(self) -> str:
        """
        Returns a string representation of the player instance.

        Returns:
            str: A string showing the player's maximum health.
        """
        return f"Player({self._max_health})"


#4.1.9 Slug(Entity)
class Slug(Entity):
    """
    Represents a slug enemy in the game. Slugs have health, poison, and can move
    or attack depending on their behavior. Specific slug types should inherit
    from this class and implement custom behavior.
    """

    def __init__(self, max_health: int):
        """
        Initializes a slug with a specified maximum health.

        Args:
            max_health (int): The maximum health of the slug.
        """
        super().__init__(max_health)
        self.can_move_next_turn = True  # Determines if the slug can move on the next turn

    def get_symbol(self) -> str:
        """
        Returns the symbol that represents a generic slug.

        Returns:
            str: The symbol of a slug.
        """
        return SLUG_SYMBOL

    def get_name(self) -> str:
        """
        Returns the name of the slug.

        Returns:
            str: The name "Slug".
        """
        return "Slug"

    def choose_move(self, candidates: list[Position], current_position: Position,
                    player_position: Position) -> Position:
        """
        Determines the slug's movement. This method should be implemented by slug subclasses.

        Args:
            candidates (list[Position]): List of valid positions the slug can move to.
            current_position (Position): The slug's current position.
            player_position (Position): The player's current position.

        Returns:
            Position: The chosen position to move to.
        """
        raise NotImplementedError("Slug subclasses must implement a choose_move method.")

    def can_move(self) -> bool:
        """
        Determines if the slug can move on this turn.

        Returns:
            bool: True if the slug can move, False otherwise.
        """
        return self.can_move_next_turn

    def end_turn(self) -> None:
        """
        Toggles the slug's ability to move on the next turn.
        Slugs can only move every other turn.
        """
        self.can_move_next_turn = not self.can_move_next_turn

    def get_poison_level(self) -> int:
        """
        Returns the current poison level affecting the slug.

        Returns:
            int: The slug's poison level.
        """
        return self.get_poison()

    def __str__(self) -> str:
        """
        Returns the string representation of the slug, showing its name.

        Returns:
            str: The name of the slug.
        """
        return self.get_name()

    def __repr__(self):
        """
        Returns a detailed representation of the slug, primarily for debugging.

        Returns:
            str: A string showing the slug type and its maximum health.
        """
        return f"{self.get_name()}({self._max_health})"


# 4.1.10 NiceSlug(Slug)
class NiceSlug(Slug):
    """
    Represents a specific type of slug called NiceSlug.
    NiceSlugs do not move and come equipped with a HealingRock to heal themselves or others.
    """

    def __init__(self):
        """
        Initializes a NiceSlug with 10 health and equips it with a HealingRock.
        """
        super().__init__(10)  # Initialize with 10 health
        self.equip(HealingRock())  # Equip the NiceSlug with a HealingRock

    def choose_move(self, candidates: list[Position],
                    current_position: Position, player_position: Position) -> Position:
        """
        Determines the NiceSlug's movement. Since NiceSlugs do not move,
        they will always return their current position.

        Args:
            candidates (list[Position]): List of valid positions the slug can move to.
            current_position (Position): The NiceSlug's current position.
            player_position (Position): The player's current position.

        Returns:
            Position: The current position (NiceSlugs do not move).
        """
        return current_position

    def get_name(self) -> str:
        """
        Returns the name "NiceSlug".

        Returns:
            str: The name "NiceSlug".
        """
        return "NiceSlug"

    def get_symbol(self) -> str:
        """
        Returns the symbol "N" that represents a NiceSlug.

        Returns:
            str: The symbol for NiceSlug.
        """
        return NICE_SLUG_SYMBOL

    def get_poison_level(self) -> int:
        """
        Returns the poison level of the NiceSlug. Since NiceSlugs are not affected by poison,
        this always returns 0.

        Returns:
            int: 0 (NiceSlugs are not poisoned).
        """
        return 0

    def __str__(self) -> str:
        """
        Returns the string representation of the NiceSlug.

        Returns:
            str: The name "NiceSlug".
        """
        return "NiceSlug"

    def __repr__(self) -> str:
        """
        Returns a detailed representation of the NiceSlug instance, primarily for debugging.

        Returns:
            str: The string "NiceSlug()".
        """
        return f"NiceSlug()"


#4.1.11 AngrySlug(Slug)
class AngrySlug(Slug):
    """
    Represents a specific type of slug called AngrySlug.
    AngrySlugs are aggressive slugs that equip a PoisonSword and try to move closer to the player.
    """

    def __init__(self):
        """
        Initializes an AngrySlug with 5 health and equips it with a PoisonSword.
        """
        super().__init__(max_health=5)
        self.equip(PoisonSword())  # Equip the AngrySlug with a PoisonSword

    def choose_move(self, candidates: list[Position], current_position: Position,
                    player_position: Position) -> Position:
        """
        Determines the AngrySlug's movement. The slug moves to the position that is
        closest to the player's position.

        Args:
            candidates (list[Position]): List of valid positions the slug can move to.
            current_position (Position): The AngrySlug's current position.
            player_position (Position): The player's current position.

        Returns:
            Position: The position closest to the player. If no valid positions, returns the current position.
        """
        if not candidates:
            return current_position

        # Calculate the closest position to the player using Euclidean distance
        closest_position = min(candidates, key=lambda pos: (
        (pos[0] - player_position[0]) ** 2 + (pos[1] - player_position[1]) ** 2, pos))
        return closest_position

    def get_symbol(self) -> str:
        """
        Returns the symbol "A" that represents an AngrySlug.

        Returns:
            str: The symbol for AngrySlug.
        """
        return ANGRY_SLUG_SYMBOL

    def get_name(self) -> str:
        """
        Returns the name "AngrySlug".

        Returns:
            str: The name "AngrySlug".
        """
        return "AngrySlug"

    def get_poison_level(self) -> int:
        """
        Returns the poison level of the AngrySlug. Since AngrySlugs are not poisoned,
        this always returns 0.

        Returns:
            int: 0 (AngrySlugs are not poisoned).
        """
        return 0

    def __str__(self):
        """
        Returns the string representation of the AngrySlug.

        Returns:
            str: The name "AngrySlug".
        """
        return "AngrySlug"

    def __repr__(self):
        """
        Returns a detailed representation of the AngrySlug instance, primarily for debugging.

        Returns:
            str: The string "AngrySlug()".
        """
        return "AngrySlug()"


# 4.1.12 ScaredSlug(Slug)
class ScaredSlug(Slug):
    """
    Represents a specific type of slug called ScaredSlug.
    ScaredSlugs are timid slugs that equip a PoisonDart and try to move away from the player.
    """

    def __init__(self):
        """
        Initializes a ScaredSlug with 3 health and equips it with a PoisonDart.
        """
        super().__init__(max_health=3)
        self.equip(PoisonDart())  # Equip the ScaredSlug with a PoisonDart

    def distance(self, pos1: Position, pos2: Position) -> float:
        """
        Calculates the Euclidean distance between two positions.

        Args:
            pos1 (Position): The first position (row, column).
            pos2 (Position): The second position (row, column).

        Returns:
            float: The Euclidean distance between pos1 and pos2.
        """
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def choose_move(self, candidates: list[Position], current_position: Position,
                    player_position: Position) -> Position:
        """
        Determines the ScaredSlug's movement. The slug moves to the position that is
        farthest from the player's position.

        Args:
            candidates (list[Position]): List of valid positions the slug can move to.
            current_position (Position): The ScaredSlug's current position.
            player_position (Position): The player's current position.

        Returns:
            Position: The position farthest from the player. If no valid positions, returns the current position.
        """
        if not candidates:
            return current_position

        # Calculate the furthest position from the player using Euclidean distance
        furthest_position = max(candidates, key=lambda pos: self.distance(pos, player_position))
        return furthest_position

    def get_symbol(self) -> str:
        """
        Returns the symbol "L" that represents a ScaredSlug.

        Returns:
            str: The symbol for ScaredSlug.
        """
        return SCARED_SLUG_SYMBOL

    def get_name(self) -> str:
        """
        Returns the name "ScaredSlug".

        Returns:
            str: The name "ScaredSlug".
        """
        return "ScaredSlug"

    def get_poison_level(self) -> int:
        """
        Returns the current poison level of the ScaredSlug.

        Returns:
            int: The ScaredSlug's poison level.
        """
        return self.get_poison()

    def __str__(self):
        """
        Returns the string representation of the ScaredSlug.

        Returns:
            str: The name "ScaredSlug".
        """
        return "ScaredSlug"

    def __repr__(self):
        """
        Returns a detailed representation of the ScaredSlug instance, primarily for debugging.

        Returns:
            str: The string "ScaredSlug()".
        """
        return f"ScaredSlug()"


#4.1.13 SlugDungeonModel()
class SlugDungeonModel:
    """
    Represents the game model for the Slug Dungeon. This model handles the game's
    core mechanics including player actions, slug movements, attacks, and turn-based
    interactions.
    """
    def __init__(self, tiles: list[list[Tile]], slugs: dict[Position, Slug],
                 player: Player, player_position: Position) -> None:
        """
        Initializes the SlugDungeonModel with the game board, slugs, player,
        and the player's starting position.

        Args:
            tiles (list[list[Tile]]): The dungeon map represented as a 2D list of tiles.
            slugs (dict[Position, Slug]): A dictionary mapping positions to slug entities.
            player (Player): The player entity in the game.
            player_position (Position): The starting position of the player.
        """
        self._tiles = tiles  # The dungeon map
        self._slugs = slugs  # Dictionary of slug entities and their positions
        self._player = player  # The player entity
        self._player_position = player_position  # Current position of the player
        self._dimensions = (len(tiles), len(tiles[0]))  # Dimensions of the dungeon map
        self._player_past_position = player_position  # Track player's past position

    def get_tiles(self) -> list[list[Tile]]:
        """
        Returns the 2D list of tiles representing the dungeon map.

        Returns:
            list[list[Tile]]: The dungeon tiles.
        """
        return self._tiles

    def get_slugs(self) -> dict[Position, Slug]:
        """
        Returns a copy of the slugs dictionary.

        Returns:
            dict[Position, Slug]: The dictionary mapping positions to slugs.
        """
        return {pos: slug for pos, slug in self._slugs.items()}

    def get_player(self) -> Player:
        """
        Returns the player entity.

        Returns:
            Player: The player entity.
        """
        return self._player

    def get_player_position(self) -> Position:
        """
        Returns the current position of the player.

        Returns:
            Position: The player's position.
        """
        return self._player_position

    def get_tile(self, position: Position) -> Tile:
        """
        Returns the tile at the specified position.

        Args:
            position (Position): The coordinates (row, column) of the tile.

        Returns:
            Tile: The tile at the specified position.
        """
        row, col = position
        return self._tiles[row][col]

    def get_dimensions(self) -> tuple[int, int]:
        """
        Returns the dimensions of the dungeon map.

        Returns:
            tuple[int, int]: The dimensions (rows, columns) of the dungeon map.
        """
        return self._dimensions

    def get_valid_slug_positions(self, slug: Slug) -> list[Position]:
        """
        Returns a list of valid positions the slug can move to.

        Args:
            slug (Slug): The slug entity.

        Returns:
            list[Position]: List of valid positions for the slug.
        """
        if not slug.can_move():
            return []

        current_position = next(pos for pos, s in self._slugs.items() if s == slug)
        valid_positions = [current_position]

        for delta in POSITION_DELTAS:
            new_pos = (current_position[0] + delta[0], current_position[1] + delta[1])
            if self._is_valid_move(new_pos):
                valid_positions.append(new_pos)

        return valid_positions

    def _is_valid_move(self, position: Position) -> bool:
        """
        Checks if a position is a valid move (not blocked, not occupied).

        Args:
            position (Position): The position to check.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        row, col = position
        if 0 <= row < self._dimensions[0] and 0 <= col < self._dimensions[1]:
            tile = self.get_tile(position)
            return (not tile.is_blocking() and position not in self._slugs
                    and position != self._player_position)
        return False

    def perform_attack(self, entity: Entity, position: Position) -> None:
        """
        Executes an attack from the given entity at the specified position.
        Entities can attack based on their equipped weapon and targets within range.

        Args:
            entity (Entity): The attacking entity (player or slug).
            position (Position): The position from which the entity attacks.
        """
        targets = entity.get_weapon_targets(position)

        for p in targets:
            x, y = p
            if 0 <= x < len(self._tiles) and 0 <= y < len(self._tiles[0]):
                if isinstance(entity, Player):
                    if p in self._slugs:
                        slug = self._slugs[p]
                        slug.apply_effects(entity.get_weapon_effect())
                        if not slug.is_alive():
                            self.get_tile(p).set_weapon(slug.get_weapon())
                            del self._slugs[p]
                elif isinstance(entity, Slug):
                    if p == self._player_position:
                        self._player.apply_effects(entity.get_weapon_effect())

    def end_turn(self) -> None:
        """
        Handles end of turn actions including applying poison effects, slug movements,
        and updating the state of the game for the next turn.
        """
        self._player.apply_poison()

        # Create a new dictionary to store updated slug positions
        new_slugs = {}

        # Handle poison effects and slug movements
        for slug_pos, slug in list(self._slugs.items()):
            slug.apply_poison()
            if not slug.is_alive():
                if slug.get_weapon():
                    self.get_tile(slug_pos).set_weapon(slug.get_weapon())
                continue  # Do not add to new dictionary

            # Handle slug movement and attack
            new_pos = slug_pos
            if slug.can_move():
                valid_positions = self.get_valid_slug_positions(slug)
                chosen_pos = slug.choose_move(valid_positions,
                                              slug_pos, self._player_past_position)
                if chosen_pos in valid_positions:
                    new_pos = chosen_pos

            # Add slug to the new position
            new_slugs[new_pos] = slug

            # Perform attack
            self.perform_attack(slug, new_pos)
            slug.end_turn()

        # Update the slugs dictionary
        self._slugs = new_slugs
        self._player_past_position = self._player_position

    def handle_player_move(self, position_delta: Position) -> None:
        """
        Moves the player based on the given position delta, picking up weapons and
        triggering attacks as necessary.

        Args:
            position_delta (Position): The change in position for the player's move.
        """
        new_position = (
            self._player_position[0] + position_delta[0],
            self._player_position[1] + position_delta[1]
        )

        if (0 <= new_position[0] < len(self._tiles)
                and 0 <= new_position[1] < len(self._tiles[0])
                and not self.get_tile(new_position).is_blocking()
                and new_position not in self._slugs):
            self._player_position = new_position
            current_tile = self.get_tile(new_position)

            # Pick up weapon
            weapon = current_tile.get_weapon()
            if weapon:
                self._player.equip(weapon)
                current_tile.remove_weapon()

            # Perform attack
            self.perform_attack(self._player, self._player_position)

            self.end_turn()

    def has_won(self) -> bool:
        """
        Checks if the player has won the game (all slugs are defeated, and the player is on the goal).

        Returns:
            bool: True if the player has won, False otherwise.
        """
        return not self._slugs and self.get_tile(self._player_position).get_symbol() == GOAL_TILE

    def has_lost(self) -> bool:
        """
        Checks if the player has lost the game (player health is 0 or below).

        Returns:
            bool: True if the player has lost, False otherwise.
        """
        return self._player.get_health() <= 0


# 4.1.14 load_level(filename: str) -> SlugDungeonModel
def load_level(filename: str) -> SlugDungeonModel:
    """
    Loads a game level from a file and initializes the SlugDungeonModel based on
    the level data.

    Args:
        filename (str): The path to the level file.

    Returns:
        SlugDungeonModel: The game model initialized from the file.
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    player_health = int(lines[0].strip())
    tiles = []
    slugs = {}
    player_position = None

    for row, line in enumerate(lines[1:]):
        tile_row = []
        for col, char in enumerate(line.strip()):
            tile = create_tile(char)
            if char == PLAYER_SYMBOL:
                player_position = (row, col)
            elif char in [NICE_SLUG_SYMBOL, ANGRY_SLUG_SYMBOL, SCARED_SLUG_SYMBOL]:
                if char == NICE_SLUG_SYMBOL:
                    slugs[(row, col)] = NiceSlug()
                elif char == ANGRY_SLUG_SYMBOL:
                    slugs[(row, col)] = AngrySlug()
                elif char == SCARED_SLUG_SYMBOL:
                    slugs[(row, col)] = ScaredSlug()
            tile_row.append(tile)
        tiles.append(tile_row)

    player = Player(player_health)
    return SlugDungeonModel(tiles, slugs, player, player_position)


#4.2 View
# 4.2.1 DungeonMap(AbstractGrid)
class DungeonMap(AbstractGrid):
    """
    Represents the graphical display of the dungeon map. This class is responsible for
    rendering the tiles, player, and slugs on the grid.
    """
    def __init__(
            self,
            master: Union[tk.Tk, tk.Frame],
            dimensions: tuple[int, int],
            size: tuple[int, int],
            **kwargs,
    ) -> None:
        """
        Initializes the DungeonMap with the master widget, grid dimensions, and size.

        Args:
            master (Union[tk.Tk, tk.Frame]): The parent widget.
            dimensions (tuple[int, int]): The dimensions of the grid (rows, columns).
            size (tuple[int, int]): The size of the grid (width, height).
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, dimensions, size, **kwargs)

    def redraw(self, tiles: list[list[Tile]],
               player_position: Position, slugs: dict[Position, Slug]) -> None:
        """
        Redraws the dungeon map, updating the tiles, player, and slugs.

        Args:
            tiles (list[list[Tile]]): The 2D list of tiles representing the dungeon map.
            player_position (Position): The current position of the player.
            slugs (dict[Position, Slug]): Dictionary of slug positions and their corresponding slugs.
        """
        self.clear()

        # Determine the dimensions of the grid
        num_rows = len(tiles)
        num_cols = len(tiles[0]) if num_rows > 0 else 0
        self.set_dimensions((num_rows, num_cols))  # Set new grid dimensions

        # Draw the tiles
        for row in range(num_rows):
            for col in range(num_cols):
                tile = tiles[row][col]
                bbb = self.get_bbox((row, col))
                if str(tile) == WALL_TILE:
                    color = WALL_COLOUR
                elif str(tile) == GOAL_TILE:
                    color = GOAL_COLOUR
                else:
                    color = FLOOR_COLOUR
                self.create_rectangle(bbb, fill=color, outline="black")
                if tile.get_weapon():
                    self.annotate_position((row, col), tile.get_weapon().get_symbol())

        # Draw the player
        player_round = self.get_bbox(player_position)
        self.create_oval(player_round, fill=PLAYER_COLOUR)
        self.annotate_position(player_position, "Player")

        # Draw the slugs
        for slug_pos, slug in slugs.items():
            slug_round = self.get_bbox(slug_pos)
            self.create_oval(slug_round, fill=SLUG_COLOUR)
            slug_name = "\n".join(slug.__class__.__name__.replace("Slug", " Slug").split())
            self.annotate_position(slug_pos, slug_name)


# 4.2.2 DungeonInfo(AbstractGrid)
class DungeonInfo(AbstractGrid):
    """
    Represents the information display grid for entities in the dungeon.
    This class shows details about entities such as their name, position, weapon, health, and poison level.
    """
    def __init__(self, master, dimensions, size, **kwargs):
        """
        Initializes the DungeonInfo grid with the master widget, dimensions, and size.

        Args:
            master: The parent widget.
            dimensions: The dimensions of the grid (rows, columns).
            size: The size of the grid (width, height).
            **kwargs: Additional keyword arguments.
        """
        super().__init__(master, dimensions, size, **kwargs)
        self._draw_headers()

    def _draw_headers(self):
        """
        Draws the header row for the information table, including column names for the entities.
        """
        headers = ["Name", "Position", "Weapon", "Health", "Poison"]
        for col_idx, header in enumerate(headers):
            self.annotate_position((0, col_idx), header, font=TITLE_FONT)

    def redraw(self, entities: dict[Position, Entity]) -> None:
        """
        Redraws the DungeonInfo grid, updating the displayed information for each entity.

        Args:
            entities (dict[Position, Entity]): Dictionary of entity positions and their corresponding entities.
        """
        self.clear()  # Clear the previous content
        self._draw_headers()  # Redraw the headers

        # Loop through each entity and display its information
        for row_idx, (position, entity) in enumerate(entities.items(), start=1):
            name = entity.get_name()  # Entity name (e.g., Player, AngrySlug)
            weapon = entity.get_weapon().get_name() if entity.get_weapon() else "None"
            health = entity.get_health()  # Entity health
            poison = entity.get_poison_level()  # Poison level

            # Information to display for each column
            info = [
                name,  # Column 1: Entity name
                f"({position[0]}, {position[1]})",  # Column 2: Position (x, y)
                weapon,  # Column 3: Weapon name (or "None" if no weapon)
                str(health),  # Column 4: Health
                str(poison)  # Column 5: Poison level
            ]

            # Annotate each piece of information in the grid
            for col_idx, data in enumerate(info):
                self.annotate_position((row_idx, col_idx), data)


# 4.2.3 ButtonPanel(tk.Frame)
class ButtonPanel(tk.Frame):
    """
    Represents a control panel with buttons for the game interface.
    This class contains buttons for loading the game and quitting the application.
    """
    def __init__(self, root: tk.Tk, on_load: Callable, on_quit: Callable) -> None:
        """
        Initializes the ButtonPanel with Load Game and Quit buttons.

        Args:
            root (tk.Tk): The root widget.
            on_load (Callable): The function to be called when the Load Game button is pressed.
            on_quit (Callable): The function to be called when the Quit button is pressed.
        """
        super().__init__(root, width=900, height=100)  # Set explicit width and height

        # Prevent the frame from resizing to fit its content
        self.pack_propagate(False)

        # Create the Load Game button
        load_button = tk.Button(self, text="Load Game", command=on_load)
        load_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        # Create the Quit button
        quit_button = tk.Button(self, text="Quit", command=on_quit)
        quit_button.pack(side=tk.RIGHT, padx=10, pady=10, expand=True)  # Manually position the Quit button

        # Set the width and height explicitly and position it with place()
        self.place(x=0, y=0, width=900, height=100)


#4.3 Controller
#4.3.1 SlugDungeon()
class SlugDungeon:
    """
    Represents the main controller for the Slug Dungeon game. This class handles
    initializing the game, managing the graphical user interface, processing user
    input, and controlling game interactions.
    """
    def __init__(self, root: tk.Tk, filename: str) -> None:
        """
        Initializes the SlugDungeon game with the main window and level file.

        Args:
            root (tk.Tk): The root Tkinter window.
            filename (str): The path to the level file to load.
        """
        self.root = root
        self.model = load_level(filename)  # Load the game model based on the level file
        self.filename = filename

        # Set the main window size
        window_width = DUNGEON_MAP_SIZE[0] + SLUG_INFO_SIZE[0]
        window_height = max(DUNGEON_MAP_SIZE[1], SLUG_INFO_SIZE[1]) + PLAYER_INFO_SIZE[1] + 50
        self.root.geometry(f"{window_width}x{window_height}")

        # Create and place DungeonMap
        self.dungeon_map = DungeonMap(root, self.model.get_dimensions(), size=DUNGEON_MAP_SIZE)
        self.dungeon_map.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

        # Create and place SlugInfo
        self.slug_info = DungeonInfo(root, dimensions=(7, 5), size=SLUG_INFO_SIZE)
        self.slug_info.grid(row=0, column=1, padx=5, pady=5)

        # Create and place PlayerInfo
        self.player_info = DungeonInfo(root, dimensions=(2, 5), size=PLAYER_INFO_SIZE)
        self.player_info.grid(row=1, column=1, padx=5, pady=5)

        # Create and place ButtonPanel
        self.button_panel = ButtonPanel(root, self.load_level, root.destroy)
        self.button_panel.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Bind key press events for player movement
        self.root.bind("<KeyPress>", self.handle_key_press)

        # Initial redraw
        self.redraw()
        self.root.update_idletasks()

    def redraw(self) -> None:
        """
        Redraws the game interface, including the dungeon map, slug information,
        and player information.
        """
        # Clear and redraw DungeonMap
        self.dungeon_map.redraw(self.model.get_tiles(),
                                self.model.get_player_position(), self.model.get_slugs())

        # Clear and redraw SlugInfo
        self.slug_info.redraw(self.model.get_slugs())

        # Clear and redraw PlayerInfo
        player_data = {self.model.get_player_position(): self.model.get_player()}
        self.player_info.redraw(player_data)

        # Force the display to update
        self.root.update_idletasks()

    def handle_key_press(self, event: tk.Event) -> None:
        """
        Handles keyboard input for player movement and interactions.

        Args:
            event (tk.Event): The key press event.
        """
        key = event.keysym.lower()
        movement = {
            'a': POSITION_DELTAS[1],  # Move left
            'd': POSITION_DELTAS[0],  # Move right
            'w': POSITION_DELTAS[3],  # Move up
            's': POSITION_DELTAS[2],  # Move down
            'space': (0, 0)  # Stay in place
        }

        if key in movement:
            move_delta = movement[key]
            self.model.handle_player_move(move_delta)
            self.redraw()
            self.root.update_idletasks()

            # Check for win or loss conditions
            if self.model.has_won() or self.model.has_lost():
                title = WIN_TITLE if self.model.has_won() else LOSE_TITLE
                message = WIN_MESSAGE if self.model.has_won() else LOSE_MESSAGE
                if messagebox.askyesno(title, message):
                    self.model = load_level(self.filename)  # Reload the level
                    self.redraw()  # Update the view
                else:
                    self.root.destroy()

    def load_level(self) -> None:
        """
        Opens a file dialog to load a new level file, updates the game model, and redraws the interface.
        """
        filename = filedialog.askopenfilename(
            title="Select Level File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        # Load the new game model
        self.model = load_level(filename)
        self.dungeon_map.set_dimensions((len(self.model.get_tiles()), len(self.model.get_tiles()[0])))
        self.redraw()


#4.4 play_game(root: tk.Tk, file_path: str) -> None
def play_game(root: tk.Tk, file_path: str) -> None:
    """
    Play the SlugDungeon game.

    Args:
        root (tk.Tk): The root window
        file_path (str): Path to the level file
    """
    root.title("Slug Dungeon")
    SlugDungeon(root, file_path)
    root.mainloop()


def main() -> None:
    """
    The main entry point for the Slug Dungeon game.
    """
    root = tk.Tk()
    # root.title("Slug Dungeon")
    play_game(root, 'levels/level1.txt')  # Start the game with the specified level

if __name__ == "__main__":
    main()

