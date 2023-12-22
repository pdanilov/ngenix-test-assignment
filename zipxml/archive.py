import random
import string
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZipFile

CHARSET = string.digits + string.ascii_letters
IDS = set()


def random_string(len: int) -> str:
    return "".join(random.choice(CHARSET) for _ in range(len))


def generate_xml_tree(id_len: int, object_name_len: int) -> ET.ElementTree:
    while True:
        id_str = random_string(id_len)
        if id_str not in IDS:
            IDS.add(id_str)
            break

    root = ET.Element("root")
    ET.SubElement(root, "var", name="id", value=id_str)
    ET.SubElement(root, "var", name="level", value=str(random.randint(1, 100)))
    objs = ET.SubElement(root, "objects")
    num_childs = random.randint(1, 10)
    for _ in range(num_childs):
        ET.SubElement(objs, "object", name=random_string(object_name_len))
    ET.indent(root)
    return ET.ElementTree(root)


def align_width(num: int) -> int:
    power = 0
    while num > 0:
        num //= 10
        power += 1
    return power


@dataclass
class ArchiveArgs:
    zip_num: int
    xml_num: int
    id_len: int
    object_name_len: int


def create_zip(zip_name: str, params: ArchiveArgs):
    with ZipFile(zip_name, mode="w") as zip:
        for _ in range(params.xml_num):
            with NamedTemporaryFile(suffix=".xml") as f:
                et = generate_xml_tree(params.id_len, params.object_name_len)
                et.write(f, xml_declaration=True)
                f.flush()
                zip.write(f.name, Path(f.name).name)


def run_archive(out_dir: Path, args: ArchiveArgs):
    w = align_width(args.zip_num)
    runs = []
    with Pool() as pool:
        for i in range(args.zip_num):
            zip_name = out_dir / f"arch{i:0{w}}"
            run = pool.apply_async(create_zip, [zip_name, args])
            runs.append(run)

        for run in runs:
            run.wait()
