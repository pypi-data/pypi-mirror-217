import struct
from pathlib import Path
from typing import TypedDict

from . import const
from .checksum import ra2_crc


def get_mix_db_data(filenames: list[str], game: const.XCCGame):
    num_files = len(filenames)
    db_size = (
        const.XCC_HEADER_SIZE
        + sum([len(filename) for filename in filenames])
        + num_files
    )
    print(db_size)

    data = struct.pack("=32s", const.XCC_ID_BYTES) + struct.pack(
        "=5I",
        db_size,
        const.XCC_FILE_TYPE,
        const.XCC_FILE_VERSION,
        game.value,
        num_files,
    )

    for filename in filenames:
        data += struct.pack(f"={len(filename) + 1}s", filename.encode())

    return data


def coalesce_input_files(
    game: const.XCCGame,
    file_map: dict[str, bytes] | None,
    input_folder: str | None,
    filepaths: list[str] | None,
):
    if sum(map(bool, [file_map, input_folder, filepaths])) > 1:
        raise ValueError(
            "Must provide exactly one of the following args: file_map, input_folder, "
            "filepaths"
        )

    if not file_map:
        if input_folder:
            folder_path = Path(input_folder)
            assert folder_path.exists(), f"{folder_path} does not exist!"

            paths = list(folder_path.rglob("*.*"))
        else:
            paths = [Path(filepath) for filepath in filepaths]
            for path in paths:
                assert path.exists(), f"{path} does not exist!"

        file_map = {}
        for path in paths:
            file_map[path.name] = path.read_bytes()

    filenames = list(file_map.keys())
    filenames.append(const.MIX_DB_FILENAME)
    print(filenames)

    db_data = get_mix_db_data(filenames, game)

    file_map[const.MIX_DB_FILENAME] = db_data

    return file_map


def packed_id(filename: str):
    crc = ra2_crc(filename)
    # CRC must be interpreted as a 32-bit signed integer for proper sorting
    # in mix file header/body
    (pid,) = struct.unpack("=i", struct.pack("=I", crc))
    return pid


class FileInfo(TypedDict):
    file_id: int
    data: bytes


def write(
    mix_filepath: str,
    game: const.XCCGame = const.XCCGame.RA2,
    file_map: dict[str, bytes] | None = None,
    folder_path: str | None = None,
    filepaths: list[str] | None = None,
):
    file_map = coalesce_input_files(game, file_map, folder_path, filepaths)
    flags = 0
    file_count = len(file_map)
    data_size = sum(len(data) for data in file_map.values())

    print(f"Writing {file_count} files to mix file; total size = {data_size}")

    header = struct.pack("=I H I", flags, file_count, data_size)

    print(f"Header: {header}")

    file_information_list = [
        FileInfo(file_id=packed_id(filename), data=data)
        for filename, data in file_map.items()
    ]
    sorted_file_info_list = sorted(
        file_information_list, key=lambda file_info: file_info["file_id"]
    )

    print(f"Sorted file info: {sorted_file_info_list}")

    file_entries: list[const.FileEntry] = []
    offset = 0
    for file_info in sorted_file_info_list:
        size = len(file_info["data"])
        file_entries.append(
            const.FileEntry(id=file_info["file_id"], offset=offset, size=size)
        )
        offset += size

    print(f"File entries: {file_entries}")

    file_entry_data = b""
    body_data = b""
    for file_entry, file_info in zip(file_entries, sorted_file_info_list):
        file_entry_data += struct.pack(
            "=iII", file_entry.id, file_entry.offset, file_entry.size
        )
        body_data += file_info["data"]

    mix_data = header + file_entry_data + body_data

    with open(mix_filepath, "wb") as fp:
        fp.write(mix_data)
