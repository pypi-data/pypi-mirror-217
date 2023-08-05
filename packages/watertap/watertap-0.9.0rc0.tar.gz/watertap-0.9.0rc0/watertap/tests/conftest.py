#################################################################################
# WaterTAP Copyright (c) 2020-2023, The Regents of the University of California,
# through Lawrence Berkeley National Laboratory, Oak Ridge National Laboratory,
# National Renewable Energy Laboratory, and National Energy Technology
# Laboratory (subject to receipt of any required approvals from the U.S. Dept.
# of Energy). All rights reserved.
#
# Please see the files COPYRIGHT.md and LICENSE.md for full copyright and license
# information, respectively. These files are also available online at the URL
# "https://github.com/watertap-org/watertap/"
#################################################################################
import logging
from pathlib import Path
from watertap.edb import ElectrolyteDB
import pytest

_log = logging.getLogger(__name__)

DOCS_DIR = "docs"  # expected documentation directory name


def get_docs_root():
    start = Path(__file__)
    p, pp = start, start.parent
    # loop while there is a parent and it's not named 'site_packages'
    while pp != p and pp.name != "site_packages":
        target = p / DOCS_DIR
        if target.exists() and target.is_dir():
            return start, target
        p, pp = pp, pp.parent
    # not found
    return start, None


@pytest.fixture(scope="session")
def docs_root():
    """Find docs root, or call pytest.skip"""
    start, result = get_docs_root()
    if result is None:
        pytest.skip(f"No directory '{DOCS_DIR}' found from '{start}'")
    yield result


def check_for_mongodb() -> bool:
    try:
        edb = ElectrolyteDB()  # will fail if no DB
        edb.get_base()  # will fail if DB is not loaded
    except Exception as err:
        _log.warning(f"Could not connect to MongoDB: {err}")
    return False


@pytest.fixture(scope="module")
def electrolytedb():
    """See if EDB can be instantiated, or call pytest.skip"""
    if not check_for_mongodb():
        pytest.skip("MongoDB is required")
