import csv
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from itertools import chain, product
from multiprocessing import Pool
from pathlib import Path
from zipfile import ZipFile, is_zipfile


@dataclass
class ParseResult:
    level: tuple[str, str]
    objects: list[tuple[str, str]]


def parse_single_zip(path: Path):
    with ZipFile(path, mode="r") as zip:
        for fname in zip.namelist():
            with zip.open(fname, mode="r") as f:
                tree = ET.parse(f)
                for var in tree.findall("var"):
                    name = var.get("name")
                    if name == "id":
                        id_ = var.get("value")
                    elif name == "level":
                        level = var.get("value")
                objs_iter = product([id_], (obj.get("name") for obj in tree.find("objects").iter("object")))
                return ParseResult(level=(id_, level), objects=list(objs_iter))


def run_parse(in_dir: Path, out_dir: Path):
    with open(out_dir / "levels.csv", mode="w") as f_lvls, open(out_dir / "objects.csv", mode="w") as f_objs:
        lvls_writer, objs_writer = csv.writer(f_lvls), csv.writer(f_objs)
        lvls_writer.writerow(["id", "level"])
        objs_writer.writerow(["id", "object_name"])

        files = (p_child for p_child in in_dir.iterdir() if is_zipfile(p_child))
        with Pool() as pool:
            results = pool.map(parse_single_zip, files)

        lvls_writer.writerows(res.level for res in results)
        objs_writer.writerows(chain.from_iterable(res.objects for res in results))
