#! python3.8
from __future__ import annotations
from typing import Tuple, NamedTuple, List, Dict, Set, Optional, Counter
from math import sqrt, prod


Edge = str


class Edges(NamedTuple):
    top: Edge
    bottom: Edge
    left: Edge
    right: Edge


class TileEdge(NamedTuple):
    edge: Edge
    position: str


Pixels = List[List[str]]


class Tile(NamedTuple):
    id: int
    image_tile: Pixels = []
    tile_edges: List[TileEdge] = []

    @staticmethod
    def empty() -> Tile:
        return Tile(id=0,
                    image_tile="",
                    tile_edges="")

    def rotate(self: Tile, times: int) -> Tile:
        image_tile = self.image_tile
        for _ in range(times):
            rotated = []
            for c in range(len(image_tile[0])):
                rotated.append([row[c] for row in reversed(image_tile)])
            image_tile = rotated
        return self._replace(image_tile=image_tile)

    def flip_horizontal(self, do: bool = False) -> Tile:
        """
        Flip the tile horizontally and return a new tile object
        """
        image_tile = [list(reversed(row)) for row in self.image_tile] if do else self.image_tile
        return self._replace(image_tile=image_tile)

    def flip_vertical(self, do: bool = False) -> Tile:
        """
        Flip the tile vertically and return a new tile object
        """
        image_tile = list(reversed(self.image_tile)) if do else self.image_tile
        return self._replace(image_tile=image_tile)

    def all_rotations(self) -> Iterator[Tile]:
        """
        Return the 8 tiles I can get from this one
        by doing rotations and flips
        """
        for flip_h in [True, False]:
            for rot in [0, 1, 2, 3]:
                yield (self
                       .flip_horizontal(flip_h)
                       .rotate(rot)
                       )

    @property
    def top(self) -> str:
        return ''.join(self.image_tile[0])

    @property
    def bottom(self) -> str:
        return ''.join(self.image_tile[-1])

    @property
    def left(self) -> str:
        return ''.join([row[0] for row in self.image_tile])

    @property
    def right(self) -> str:
        return ''.join([row[-1] for row in self.image_tile])

    def edges(
        self,
        reverse: bool = False
    ) -> Edges:
        """
        Returns the edges of the tile as strings.
        If reverse == True, rotates the tile by 180 degrees first,
        which results in all the edges being in the opposite direction
        """
        if reverse:
            return self.rotate(2).edges()
        return Edges(
            top=self.top, bottom=self.bottom, right=self.right, left=self.left
        )


Image = List[List[Optional[Tile]]]


def parse_block(block: str) -> Tile:
    blocklines = block.strip().split("\n")
    id = 0
    image = []
    for line in blocklines:
        if line.startswith("Tile "):
            id = int(line[5:-1])
        else:
            image.append(line)

    edges = []

    edges.append(TileEdge(position="UP",
                          edge=image[0]))
    edges.append(TileEdge(position="UP_FLIP",
                          edge=image[0][::-1]))
    edges.append(TileEdge(position="DOWN",
                          edge=image[-1]))
    edges.append(TileEdge(position="DOWN_FLIP",
                          edge=image[-1][::-1]))
    edges.append(TileEdge(position="LEFT",
                          edge=''.join([e[0] for e in image])))
    edges.append(TileEdge(position="LEFT_FLIP",
                          edge=''.join([e[0] for e in image[::-1]])))
    edges.append(TileEdge(position="RIGHT",
                          edge=''.join([e[-1] for e in image])))
    edges.append(TileEdge(position="RIGHT_FLIP",
                          edge=''.join([e[-1] for e in image[::-1]])))

    return Tile(id=id,
                image_tile=image,
                tile_edges=edges)


def parse_input(input: str) -> List[Tile]:
    tiles = []
    blocks = input.split("\n\n")

    for block in blocks:
        tile = parse_block(block)
        tiles.append(tile)

    return tiles


def assemble_tiles(tiles: List[Tile]) -> List[int]:
    assembled_tiles = []
    positions = {}

    for i in range(len(tiles) - 1):
        for j in range(i + 1, len(tiles)):
            edges_i = [edge.edge for edge in tiles[i].tile_edges]
            edges_j = [edge.edge for edge in tiles[j].tile_edges]

            if len(set(edges_i).intersection(set(edges_j))) != 0:
                assembled_tiles.append(tiles[i].id)
                assembled_tiles.append(tiles[j].id)

                target = list(set(edges_i).intersection(set(edges_j)))[0]
                t1 = [edge.position for edge in tiles[i].tile_edges if edge.edge == target]
                t2 = [edge.position for edge in tiles[j].tile_edges if edge.edge == target]

                positions[(tiles[i].id, tiles[j].id)] = t1
                positions[(tiles[j].id, tiles[i].id)] = t2

    return assembled_tiles, positions


def corner_tiles(tiles: List[int]) -> List[int]:
    corner_tiles = []
    for i in range(len(tiles)):
        if tiles.count(tiles[i]) == 2 and tiles[i] not in corner_tiles:
            corner_tiles.append(tiles[i])

    return corner_tiles


def find_tile_by_id(tiles: List[Tile], id: int) -> Tile:
    return [tile for tile in tiles if tile.id == id][0]


def print_image(image: Image):
    print("IMAGE STATUS:")
    for row in image:
        print([tile.id for tile in row if tile])


class Constraint(NamedTuple):
    """
    Says that the tile at location (i, j)
    must have sides that match the specified
    top / bottom / left / right
    """
    i: int
    j: int
    top: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None
    right: Optional[str] = None

    def satisfied_by(self, tile: Tile) -> bool:
        """
        Does the tile satisfy this constraint
        """
        if self.top and tile.top != self.top:
            return False
        if self.bottom and tile.bottom != self.bottom:
            return False
        if self.left and tile.left != self.left:
            return False
        if self.right and tile.right != self.right:
            return False
        return True

    @property
    def num_constraints(self) -> int:
        return (
            (self.top is not None) +
            (self.bottom is not None) +
            (self.left is not None) +
            (self.right is not None)
        )


def find_constraints(image: Image) -> Iterator[Constraint]:
    """
    Create constraints from a (partially filled in) Assembly.
    No constraints for already-filled-in tiles or unconstrained locations.
    """
    n = len(image)

    for i, row in enumerate(image):
        for j, tile in enumerate(row):
            # already have a tile here
            if image[i][j]:
                continue
            constraints: Dict[str, str] = {}
            if i > 0 and (nbr := image[i-1][j]):
                constraints["top"] = nbr.bottom
            if i < n-1 and (nbr := image[i+1][j]):
                constraints["bottom"] = nbr.top
            if j > 0 and (nbr := image[i][j-1]):
                constraints["left"] = nbr.right
            if j < n-1 and (nbr := image[i][j+1]):
                constraints["right"] = nbr.left

            if constraints:
                yield Constraint(i, j, **constraints)


def find_corners(tiles: List[Tile]) -> List[Tile]:
    """
    Return corners oriented so that
    they would be the top left corner
    """
    # count up all the edges / reverse edges that occur
    # for example, if a tile had the top edge "ABCD",
    # we would count "ABCD" once and also "DCBA" once
    edge_counts = Counter(
        edge
        for tile in tiles
        for reverse in [True, False]
        for edge in tile.edges(reverse)
    )

    corners = []

    for tile in tiles:
        sides_with_no_matches = 0
        for edge in tile.edges():
            if edge_counts[edge] == 1 and edge_counts[edge[::-1]] == 1:
                sides_with_no_matches += 1

        if sides_with_no_matches == 2:
            # rotate to get corner edges at top and left
            for rot in [0, 1, 2, 3]:
                tile = tile.rotate(rot)
                edges = tile.edges()

                if edge_counts[edges.left] == 1 and edge_counts[edges.top] == 1:
                    corners.append(tile)
                    break

    return corners


def assemble_image(tiles: List[Tile]) -> Image:

    num_tiles = len(tiles)
    size = int(sqrt(num_tiles))
    corners = find_corners(tiles)
    assert 4 == len(corners)

    # Pick a corner, any corner
    tile = corners[0]

    # Create an empty assembly
    image: Image = [[None for _ in range(size)] for _ in range(size)]

    # Put this corner tile in the top left
    image[0][0] = tile

    # Keep track of which tiles I've already placed
    placed: Dict[int, Tuple[int, int]] = {tile.id: (0, 0)}

    # Repeat until all tiles have been placed
    while len(placed) < num_tiles:
        # Just care about unplaced tiles
        tiles = [t for t in tiles if t.id not in placed]

        # Find the constraints based on all the tiles placed so far
        # and order them by descending # of constraints
        constraints = list(find_constraints(image))
        constraints.sort(key=lambda c: c.num_constraints, reverse=True)

        # Did I find a tile to add, so we can break out of inner loops
        found_one = False

        # Try constraints one at a time and see if we can find a tile
        # that satisfies them
        for constraint in constraints:
            for tile in tiles:
                # try all rotations for this tile, to see if any satisfies this constraint
                for rot in tile.all_rotations():
                    if constraint.satisfied_by(rot):
                        # place this rotation (which is a tile) at i, j
                        image[constraint.i][constraint.j] = rot
                        placed[rot.id] = (constraint.i, constraint.j)
                        found_one = True
                        break
                if found_one:
                    break
            if found_one:
                break

    return image


def crop_and_join(image: Image) -> List[List[str]]:
    """
    Glue together the Tiles into a single grid of pixels,
    removing the edges of each tile
    """
    N = len(image)
    n = len(image[0][0].image_tile)
    nout = (n - 2) * N
    final_image = [['' for _ in range(nout)] for _ in range(nout)]
    for i, row in enumerate(image):
        for j, tile in enumerate(row):
            cropped = [line[1:-1] for line in tile.image_tile[1:-1]]
            for ii, crow in enumerate(cropped):
                for jj, pixel in enumerate(crow):
                    final_image[i * (n-2) + ii][j * (n-2) + jj] = pixel

    return final_image


SEA_MONSTER_RAW = """                  #
#    ##    ##    ###
 #  #  #  #  #  #"""

# offsets for a sea monster
SEA_MONSTER = [
    (i, j)
    for i, row in enumerate(SEA_MONSTER_RAW.split("\n"))
    for j, c in enumerate(row)
    if c == '#']


def find_sea_monsters(pixels: Pixels) -> Iterator[Tuple[int, int]]:
    """
    Return the indices of the top left corner of each sea monster
    """
    for i, row in enumerate(pixels):
        for j, c in enumerate(row):
            try:
                if all(pixels[i + di][j + dj] == '#' for di, dj in SEA_MONSTER):
                    yield (i, j)
            except IndexError:
                continue


def image_roughness(glued: Pixels) -> int:
    """
    Count the #s that are not part of a sea monster
    """
    # put the pixels in a Tile so we can use Tile methods
    tile = Tile(0, glued)

    # for each of the 8 rotation/flips, find the list of sea monster top lefts
    finds = [(t, list(find_sea_monsters(t.image_tile))) for t in tile.all_rotations()]

    # only keep the ones that had sea monsters
    finds = [(t, sm) for t, sm in finds if sm]

    # hopefully only one of them had sea monsters
    assert len(finds) == 1

    # and that's our tile (and sea monster locations)
    t, sms = finds[0]

    # now we can computer all pixels that are showing a sea monster
    sea_monster_pixels = {(i + di, j + dj)
                          for i, j in sms
                          for di, dj in SEA_MONSTER}

    # and count all the '#'s that are not sea monster pixels
    return sum(c == '#' and (i, j) not in sea_monster_pixels
               for i, row in enumerate(t.image_tile)
               for j, c in enumerate(row))


def get_terrain_not_monster(tiles: List[Tile]) -> int:

    arranged_tiles = assemble_image(tiles)
    image = crop_and_join(arranged_tiles)
    roughness = image_roughness(image)
    return roughness


with open("day-20/example.txt") as f:
    tiles = parse_input(f.read())
    assembled_tiles, positions = assemble_tiles(tiles)
    corners = corner_tiles(assembled_tiles)
    assert 4 == len(corners)
    assert 20899048083289 == prod(corners)
    assert 273 == get_terrain_not_monster(tiles)


with open("day-20/input.txt") as f:
    tiles = parse_input(f.read())
    assembled_tiles, positions = assemble_tiles(tiles)
    corners = corner_tiles(assembled_tiles)
    assert 4 == len(corners)
    print("Part 1: Product of the IDs of corner images: ",
          prod(corners))
    print("Part 2: The terrain not covered by monsters is: ",
          get_terrain_not_monster(tiles))
