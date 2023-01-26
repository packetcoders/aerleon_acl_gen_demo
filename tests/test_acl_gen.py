import os
import subprocess
import sys
from pathlib import Path

sys.path.append(f"{Path(__file__).parent.parent}")

from build_acl import acl  # no qa


def line_count(file):
    """
    Count the number of lines in a file.

    :param file: The file to count the number of lines in.
    :type file: str
    :return: The number of lines in the file.
    :rtype: int
    """
    with open(file, "r") as f:
        num_lines = sum(1 for _ in f)
    return num_lines


def test_acl_generation_via_cli(tmpdir):
    """
    Test the generation of an ACL via the command line interface.

    :param tmpdir: A temporary directory to store the generated ACL in.
    :type tmpdir: str
    """
    subprocess.run(["aclgen", "--output_directory", tmpdir], check=True)

    assert os.path.isfile(f"{tmpdir}/asa.pol.asa")
    assert os.path.isfile(f"{tmpdir}/srx.pol.srx")
    assert line_count(f"{tmpdir}/asa.pol.asa") == 47
    assert line_count(f"{tmpdir}/srx.pol.srx") == 107


def test_acl_generation_via_python():
    """
    Test the generation of an ACL via the python code.
    """
    assert len(str(acl).split("\n")) == 31
