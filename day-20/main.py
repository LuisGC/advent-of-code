from typing import NamedTuple, List
import numpy


class TileEdge(NamedTuple):
    edge: str
    position: str


class Tile(NamedTuple):
    id: int
    image_tile: List[str] = []
    tile_edges: List[TileEdge] = []


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

    edges.append(("UP", image[0]))
    edges.append(("UP", image[0][::-1]))
    edges.append(("DOWN", image[-1]))
    edges.append(("DOWN", image[-1][::-1]))
    edges.append(("LEFT", ''.join([e[0] for e in image])))
    edges.append(("LEFT", ''.join([e[0] for e in image[::-1]])))
    edges.append(("RIGHT", ''.join([e[-1] for e in image])))
    edges.append(("RIGHT", ''.join([e[-1] for e in image[::-1]])))

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

    for i in range(len(tiles) - 1):
        for j in range(i + 1, len(tiles)):
            edges_i = [edge[1] for edge in tiles[i].tile_edges]
            edges_j = [edge[1] for edge in tiles[j].tile_edges]

            if len(set(edges_i).intersection(set(edges_j))) != 0:
                assembled_tiles.append(tiles[i].id)
                assembled_tiles.append(tiles[j].id)

    return assembled_tiles


def corner_tiles(tiles: List[int]) -> List[int]:
    corner_tiles = []
    for i in range(len(tiles)):
        if tiles.count(tiles[i]) == 2 and tiles[i] not in corner_tiles:
            corner_tiles.append(tiles[i])

    return corner_tiles


with open("day-20/example.txt") as f:
    tiles = parse_input(f.read())
    assembled_tiles = assemble_tiles(tiles)
    corners = corner_tiles(assembled_tiles)
    assert 20899048083289 == numpy.prod(corners)


with open("day-20/input.txt") as f:
    tiles = parse_input(f.read())
    assembled_tiles = assemble_tiles(tiles)
    corners = corner_tiles(assembled_tiles)
    print("Part 1: Product of the IDs of corner images: ",
          numpy.prod(corners))
