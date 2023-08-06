"""
Read and write Minecraft ``.mcstructure`` files.
"""

# TODO: coordinates might be in wrong order (XYZ -> ZYX)
# TODO: maybe make Block attributes properties
# TODO: rename structure attr to blocks or something similar
# TODO: make Structure._structure public
# TODO: second layer (waterlogged blocks)
# TODO: additional block data
# TODO: entities
# TODO: rename set_blocks to fill_blocks or create alias
# TODO: export as 3d model (might be extension)
# TODO: add shadow to logo

from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from itertools import repeat
import json
from typing import Any, BinaryIO, Tuple

import numpy as np
from numpy.typing import NDArray
from pynbt import BaseTag, NBTFile, TAG_Compound, TAG_Int, TAG_List, TAG_String  # type: ignore


Coordinate = Tuple[int, int, int]


COMPABILITY_VERSION: int = 17959425
"""
The compability version for a block. The four bytes making up this
integer determine the game version number. For example, ``17879555`` is
``01 10 D2 03`` in hex meaning ``1.16.210.03``.
"""

STRUCTURE_MAX_SIZE: tuple[int, int, int] = (64, 384, 64)
"""The maximum size a structure can have."""


# TODO: cover all tags
def _into_pyobj(tag: BaseTag) -> Any:
    """
    Turns an NBT tree into a python tree.
    """
    if isinstance(tag, (TAG_Compound, dict)):
        res = {}
        for key, value in tag.items():
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res[key] = value
        return res

    if isinstance(tag, (TAG_List, list)):
        res = []
        for value in tag:
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res.append(value)
        return res

    if isinstance(tag, BaseTag):
        return tag.value

    return tag


# TODO: cover all types
def _into_tag(obj: Any) -> BaseTag:
    """
    Turn a python tree into an NBT tree.
    """
    if isinstance(obj, int):
        return TAG_Int(obj)

    if isinstance(obj, str):
        return TAG_String(obj)

    return obj


def is_valid_structure_name(name: str, *, with_prefix: bool = False) -> bool:
    """
    Validates the structure name.

    .. seealso: https://minecraft.fandom.com/wiki/Structure_Block

    Parameters
    ----------
    name
        The name of the structure.

    with_prefix
        Whether to take the prefix (e.g. ``mystructure:``)
        into account.
    """
    if with_prefix:
        name = name.replace(":", "", 1)

    return all((char.isalnum() and char in "-_") for char in name)


def has_valid_size(size: tuple[int, int, int]) -> bool:
    """Returns ``False`` if ``size`` is too big.

    .. seealso:: :const:`STRUCTURE_MAX_SIZE`
    """
    return all(map(lambda n: n[0] <= n[1], zip(size, STRUCTURE_MAX_SIZE)))


@dataclass(init=False)
class Block:
    """
    Attributes
    ----------
    name
        The name of the block.

    states
        The states of the block.

    Examples
    --------
    .. code-block::

        Block("minecraft:wool", color="red")
        Block("minecraft:grass")

    """

    identifier: str
    states: dict[str, Any]

    def __init__(self, identifier: str, **states: Any):
        """
        Parameters
        ----------
        identifier
            The identifier of the block (e.g. "minecraft:wool").

        states
            The block states such as ``color`` or ``stone_type``.
            This varies by every block.

            .. seealso:: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockstateslist
        """
        self.identifier = identifier
        self.states = states

    def __str__(self) -> str:
        return self.stringify()

    def stringify(
        self,
        *,
        with_namespace: bool = True,
        with_states: bool = True,
    ) -> str:
        """Returns a human-readable representation of the structure.

        Parameters
        ----------
        with_namespace
            Whether to include the block's namespace.

        with_states
            Whether to include the block's states.
        """
        result = ""
        if with_namespace and (ns := self.namespace) is not None:
            result += ns + ":"
        result += self.name
        if with_states:
            result += f" [{json.dumps(self.states)[1:-1]}]"
        return result

    @property
    def namespace_and_name(self) -> tuple[str | None, str]:
        """The namespace and the name of the block.

        Examples
        --------
        .. code-block:: python

            >>> from mcstructure import Block
            >>>
            >>> block = Block("minecraft:wool", color="red")
            >>> block.namespace_and_name
            ("minecraft", "wool")
            >>>
            >>> block = Block("foobar")
            >>> block.namespace_and_name
            (None, "foobar")

        """
        if ":" in self.identifier:
            ns, name = self.identifier.split(":", 1)
            return ns, name

        return (None, self.identifier)

    @property
    def name(self) -> str:
        """The name of the block.

        Examples
        --------
        .. code-block:: python

                >>> from mcstructure import Block
                >>>
                >>> block = Block("minecraft:wool", color="red")
                >>> block.name
                "wool"
                >>>
                >>> block = Block("foobar")
                >>> block.name
                "foobar"

        """
        return self.namespace_and_name[1]

    @property
    def namespace(self) -> str | None:
        """The namespace of the block.

        Examples
        --------
        .. code-block:: python

                >>> from mcstructure import Block
                >>>
                >>> block = Block("minecraft:wool", color="red")
                >>> block.namespace
                "minecraft"
                >>>
                >>> block = Block("foobar")
                >>> (block.namespace,)
                (None,)

        """
        return self.namespace_and_name[0]


class Structure:
    """Class representing a Minecraft structure that consists of blocks and entities.

    Attributes
    ----------
    structure
        The numpy array representing the blocks in the structure. Each entry is an ID
        associated with a block present in :meth:`palette`.
    """

    def __init__(
        self,
        size: tuple[int, int, int],
        fill: Block | None = Block("minecraft:air"),
    ) -> None:
        """
        Parameters
        ----------
        size
            The size of the structure.

        fill
            Fill the structure with this block at
            creation of a new structure object.

            If this is set to ``None`` the structure
            is filled with "Structure Void" blocks.

            ``'minecraft:air'`` is used as default.
        """
        if not has_valid_size(size):
            raise ValueError(f"structure too large, max size: {STRUCTURE_MAX_SIZE}")

        self.structure: NDArray[np.intc]

        self._size = size
        self._palette: list[Block] = []

        if fill is None:
            self.structure = np.full(size, -1, dtype=np.intc)

        else:
            self.structure = np.zeros(size, dtype=np.intc)
            self._palette.append(fill)

    @classmethod
    def load(cls, file: BinaryIO):
        """
        Loads a structure from a file.

        Examples
        --------
        .. code-block:: python

            from mcstructure import Structure

            with open("house.mcstructure", "rb") as f:
                struct = Structure.load(f)

        Parameters
        ----------
        file
            File object to read.
        """
        nbt = NBTFile(file, little_endian=True)
        size: tuple[int, int, int] = tuple(x.value for x in nbt["size"])  # type: ignore

        struct = cls(size)

        struct.structure = np.array(
            [_into_pyobj(x) for x in nbt["structure"]["block_indices"][0]],
            dtype=np.intc,
        ).reshape(size)

        struct._palette.extend(
            [
                Block(block["name"].value, **_into_pyobj(block["states"].value))
                for block in nbt["structure"]["palette"]["default"]["block_palette"]
            ]
        )

        return struct

    @property
    def size(self) -> tuple[int, int, int]:
        """The size of the structure."""
        return self._size

    @property
    def palette(self) -> list[Block]:
        """A copy of the palette."""
        palette = self._palette.copy()
        return palette

    def __repr__(self) -> str:
        return repr(self._get_str_array())

    def __str__(self) -> str:
        return str(self._get_str_array())

    def _get_str_array(
        self, *, with_namespace: bool = False, with_states: bool = False
    ) -> NDArray[Any]:
        """
        Returns a numpy array where each entry is a
        readable string of the corresponding block.

        Parameters
        ----------
        with_namespace
            Adds the namespace to the string if present.

        with_states
            Adds the block states to the string if present.
        """
        arr = self.get_structure().copy()
        vec = np.vectorize(
            partial(
                Block.stringify, with_namespace=with_namespace, with_states=with_states
            )
        )
        return vec(arr)

    def _add_block_to_palette(self, block: Block | None) -> int:
        """
        Adds a block to the palette.

        Parameters
        ----------
        block
            The block to add. If this is set to ``None``
            "Structure Void" will be used.

        Returns
        -------
        The position of the block in the palette. This is
        ``-1`` when ``None`` is used as ``block``.
        """
        if block is None:
            return -1

        if block in self._palette:
            return self._palette.index(block)

        self._palette.append(block)
        return len(self._palette) - 1

    def get_structure(self) -> NDArray[Any]:
        """
        Returns the structure as a numpy array filled
        with the corresponding block objects.
        """
        arr = np.full(
            self.structure.shape, Block("minecraft:structure_void"), dtype=object
        )
        for key, block in enumerate(self._palette):
            arr[self.structure == key] = block
        return arr

    def dump(self, file: BinaryIO) -> None:
        """
        Serialize the structure as a NBT file.

        Examples
        --------
        .. code-block:: python

            from mcstructure import Structure

            struct = Structure((5, 5, 5), None)
            with open("house.mcstructure", "wb") as f:
                struct.dump(f)

        Parameters
        ----------
        file
            File object to write to.
        """
        nbt = NBTFile(
            value=dict(
                format_version=TAG_Int(1),
                size=TAG_List(TAG_Int, map(TAG_Int, self._size)),
                structure=TAG_Compound(
                    dict(
                        block_indices=TAG_List(
                            TAG_List,
                            [
                                TAG_List(
                                    TAG_Int, map(TAG_Int, self.structure.flatten())
                                ),
                                TAG_List(
                                    TAG_Int,
                                    map(TAG_Int, repeat(-1, self.structure.size)),
                                ),
                            ],
                        ),
                        entities=TAG_List(TAG_Compound, []),
                        palette=TAG_Compound(
                            dict(
                                default=TAG_Compound(
                                    dict(
                                        block_palette=TAG_List(
                                            TAG_Compound,
                                            [
                                                TAG_Compound(
                                                    dict(
                                                        name=TAG_String(
                                                            block.identifier
                                                        ),
                                                        states=TAG_Compound(
                                                            {
                                                                state_name: _into_tag(
                                                                    state_value
                                                                )
                                                                for state_name, state_value in block.states.items()
                                                            }
                                                        ),
                                                        version=TAG_Int(
                                                            COMPABILITY_VERSION
                                                        ),
                                                    )
                                                )
                                                for block in self._palette
                                            ],
                                        ),
                                        block_position_data=TAG_Compound({}),
                                    )
                                )
                            )
                        ),
                    )
                ),
                structure_world_origin=TAG_List(TAG_Int, [0, 0, 0]),
            ),
            little_endian=True,
        )
        nbt.save(file, little_endian=True)

    def get_block(self, coordinate: Coordinate) -> Block | None:
        """
        Returns the block in a specific position.

        Parameters
        ----------
        coordinate
            The coordinte of the block.
        """
        x, y, z = coordinate
        return self._palette[self.structure[x, y, z]]

    def set_block(
        self,
        coordinate: Coordinate,
        block: Block | None,
    ) -> Structure:
        """
        Places a block in the structure.

        Parameters
        ----------
        coordinate
            Relative coordinates of the block's position.

        block
            The block to place. If this is set to ``None``
            "Structure Void" blocks will be used.
        """
        x, y, z = coordinate

        ident = self._add_block_to_palette(block)

        self.structure[x, y, z] = ident
        return self

    def set_blocks(
        self,
        from_coordinate: Coordinate,
        to_coordinate: Coordinate,
        block: Block,
    ) -> Structure:
        """
        Fills an area in the structure with blocks.

        Notes
        -----
        Both start and end points are included.

        Parameters
        ----------
        from_coordinate
            Relative coordinates of the start edge.

        to_coordinate
            Relative coordinates of the end edge.

        block
            The block to place. If this is set to ``None``
            "STructure Void" blocks will be used to fill.
        """
        fx, fy, fz = from_coordinate
        tx, ty, tz = to_coordinate

        ident = self._add_block_to_palette(block)
        self.structure[fx : tx + 1, fy : ty + 1, fz : tz + 1] = np.array(
            [
                [
                    [ident for k in range(abs(fz - tz) + 1)]
                    for j in range(abs(fy - ty) + 1)
                ]
                for i in range(abs(fx - tx) + 1)
            ],
            dtype=np.intc,
        ).reshape([abs(i) + 1 for i in (fx - tx, fy - ty, fz - tz)])
        return self
