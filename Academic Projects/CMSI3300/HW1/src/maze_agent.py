import itertools
from constants import Constants
from maze_clause import MazeClause
from maze_knowledge_base import MazeKnowledgeBase
from typing import *


class MazeAgent:
    """`
    BlindBot MazeAgent meant to employ Propositional Logic,
    Planning, and Active Learning to navigate the Pitsweeper
    Problem. Have fun!
    """

    def __init__(self, env: "Environment", perception: dict) -> None:
        """
        Initializes the MazeAgent with any attributes it will need to
        navigate the maze.

        Parameters:
            env (Environment):
                The Environment in which the agent is operating; make sure
                to see the spec / Environment class for public methods that
                your agent will use to solve the maze!
            perception (dict):
                The starting perception of the agent, which is a
                small dictionary with keys:
                  - loc:  the location of the agent as a (c,r) tuple
                  - tile: the type of tile the agent is currently standing upon
        """
        self.env: "Environment" = env
        self.goal: tuple[int, int] = env.get_goal_loc()

        # The agent's maze can be manipulated as a tracking mechanic
        # for what it has learned; changes to this maze will be drawn
        # by the environment and is simply for visuals / debugging
        self.maze: list = env.get_agent_maze()

        # Standard set of attributes you'll want to maintain
        self.kb: "MazeKnowledgeBase" = MazeKnowledgeBase()
        self.possible_pits: dict[tuple[int, int], int] = dict()
        self.safe_tiles: set[tuple[int, int]] = set()
        self.guaranteed_pits: set[tuple[int, int]] = set()

        self.safe_tiles.add(self.goal)
        self.safe_tiles.add(self.env.get_player_loc())
        self.manhattan_distance_dictionary: dict[tuple[int, int], int] = dict()
        self.playable_tiles: set[tuple[int, int]] = env.get_playable_locs()
        self.move_history: list[tuple[int, int]] = list()

        self.kb.tell(
            MazeClause(
                [
                    ((Constants.PIT_BLOCK, location), False)
                    for location in self.env.get_cardinal_locs(self.goal, 1)
                ]
            )
        )

        self.kb.simplify_self(self.guaranteed_pits, self.safe_tiles)

        self.think(perception)

    ##################################################################
    # Methods
    ##################################################################

    def think(self, perception: dict) -> tuple[int, int]:
        """
        The main workhorse method of how your agent will process new information
        and use that to make deductions and decisions. In gist, it should follow
        this outline of steps:
        1. Process the given perception, i.e., the new location it is in and the
           type of tile on which it's currently standing (e.g., a safe tile, or
           warning tile like "1" or "2")
        2. Update the knowledge base and record-keeping of where known pits and
           safe tiles are located, as well as locations of possible pits.
        3. Query the knowledge base to see if any locations that possibly contain
           pits can be deduced as safe or not.
        4. Use all of the above to prioritize the next location along the frontier
           to move to next.

        Parameters:
            perception (dict):
                A dictionary providing the agent's current location
                and current tile type being stood upon, of the format:
                {"loc": (x, y), "tile": tile_type}

        Returns:
            tuple[int, int]:
                The maze location along the frontier that your agent will try to
                move into next.
        """
        curr_loc: tuple[int, int] = perception["loc"]
        cardinal_locs: set[tuple[int, int]] = self.env.get_cardinal_locs(curr_loc, 1)

        match perception["tile"]:
            case Constants.SAFE_BLOCK:
                self.safe_tiles.add(curr_loc)
                for location in cardinal_locs:
                    self.kb.tell(MazeClause([((Constants.PIT_BLOCK, location), False)]))
                self.safe_tiles |= cardinal_locs

            case Constants.PIT_BLOCK:
                self.guaranteed_pits.add(curr_loc)
                self.maze[curr_loc[1]][curr_loc[0]] = Constants.PIT_BLOCK
                self.kb.tell(MazeClause([((Constants.PIT_BLOCK, curr_loc), True)]))

            case _:  # Only warn tiles remain
                self.safe_tiles.add(curr_loc)
                self.kb.tell(MazeClause([((Constants.PIT_BLOCK, curr_loc), False)]))
                self.perceive_warning(
                    cardinal_locs,
                    perception,
                )

        for tile in self.possible_pits:
            self.is_safe_tile(tile)

        self.kb.simplify_self(self.guaranteed_pits, self.safe_tiles)

        self.possible_pits = {
            key: value
            for key, value in self.possible_pits.items()
            if key not in (self.safe_tiles | self.guaranteed_pits)
        }

        frontier: set[tuple[int, int]] = self.env.get_frontier_locs()
        safe_frontier: set[tuple[int, int]] = self.safe_tiles & frontier
        mh_dist_dict = {
            (abs(self.goal[0] - tile[0]) + abs(self.goal[1] - tile[1])): tile
            for tile in safe_frontier
        }

        if not safe_frontier:
            for key in sorted(self.possible_pits, key=lambda item: item[1]):
                if key in frontier:
                    return key
        return mh_dist_dict[min(mh_dist_dict)]

    def perceive_warning(
        self,
        cardinal_locs: set[tuple[int, int]],
        perception: dict,
    ) -> None:
        """Helper method called only when agent lands on a warning tile. Deduces the state
        of adjacent tiles given current information and updates the knowledge base,
        guaranteed_pits, safe_tiles accordingly:

        1. Guaranteed pits/safe spaces by process of elimination.
        2. Inserts information into the knowledgebase based on how many warnings were triggered.

        Parameters:
            cardinal_locs (set[tuple[int, int]]):
                Set of all playable tiles directly adjacent to the player's current tile.
            perception (dict):
                The current perception of the agent, which is a
                small dictionary with keys:
                  - loc:  the location of the agent as a (c,r) tuple
                  - tile: the type of tile the agent is currently standing upon
        """
        pit_count: int = int(perception["tile"])
        see_pits: bool = (len(cardinal_locs & self.safe_tiles) + pit_count) == len(
            cardinal_locs
        )
        see_safe: bool = len(cardinal_locs & self.guaranteed_pits) == pit_count

        if see_pits:
            self.guaranteed_pits |= cardinal_locs - self.safe_tiles

        elif see_safe:
            self.safe_tiles |= cardinal_locs - self.guaranteed_pits

        else:
            cardinal_locs -= self.safe_tiles

            if pit_count <= int(Constants.WRN_TWO_BLOCK):
                self.flag_tile(cardinal_locs)
                pairs: list[tuple[tuple[int, int], tuple[int, int]]] = list(
                    itertools.combinations(cardinal_locs, 2)
                )

                is_wrn_1 = perception["tile"] == Constants.WRN_ONE_BLOCK

                for pair in pairs:
                    self.kb.tell(
                        MazeClause(
                            [
                                (("P", (pair[0])), not is_wrn_1),
                                (("P", (pair[1])), not is_wrn_1),
                            ]
                        )
                    )
                self.kb.tell(
                    MazeClause(
                        [(("P", location), is_wrn_1) for location in cardinal_locs]
                    )
                )

            else:
                see_pits = True
                self.guaranteed_pits |= cardinal_locs

        if see_pits or see_safe:
            for tile in cardinal_locs:
                self.kb.tell(
                    MazeClause([(("P", (tile)), tile in self.guaranteed_pits)])
                )

        self.kb.simplify_self(self.guaranteed_pits, self.safe_tiles)

    def flag_tile(self, cardinal_locs: set[tuple[int, int]]) -> None:
        """Increases the "flag count" of all adjacent playable tiles, indicating that they are more likely to
        contain a pit.

        Parameter:
            cardinal_locs (set[tuple[int, int]]):
                Set of all playable tiles directly adjacent to the player's current tile.
        """
        for location in cardinal_locs:
            self.possible_pits[location] = (
                1
                if location not in self.possible_pits
                else (self.possible_pits[location] + 1)
            )

    def is_safe_tile(self, loc: tuple[int, int]) -> Optional[bool]:
        """
        Determines whether or not the given maze location can be concluded as
        safe (i.e., not containing a pit), following the steps:
        1. Check to see if the location is already a known pit or safe tile,
           responding accordingly
        2. If not, performs the necessary queries on the knowledge base in an
           attempt to deduce its safety

        Parameters:
            loc (tuple[int, int]):
                The maze location in question

        Returns:
            One of three return values:
            1. True if the location is certainly safe (i.e., not pit)
            2. False if the location is certainly dangerous (i.e., pit)
            3. None if the safety of the location cannot be currently determined
        """
        if loc in self.guaranteed_pits:
            return False
        elif loc in self.safe_tiles:
            return True

        true_pit: MazeClause = MazeClause([((Constants.PIT_BLOCK, (loc)), True)])
        false_pit: MazeClause = MazeClause([((Constants.PIT_BLOCK, (loc)), False)])

        if self.kb.ask(true_pit):
            self.kb.tell(true_pit)
            self.guaranteed_pits.add(loc)
            return True

        if self.kb.ask(false_pit):
            self.kb.tell(false_pit)
            self.safe_tiles.add(loc)
            return False

        return None


# Declared here to avoid circular dependency
from environment import Environment
