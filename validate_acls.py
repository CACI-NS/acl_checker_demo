import json
import logging
import re
import sys
from typing import List
from pybatfish.client import asserts
from pybatfish.client.commands import bf_session as bf
from pybatfish.datamodel.flow import HeaderConstraints
from pybatfish.question import load_questions

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("pybatfish")

SNAPSHOT_DIR = "./snapshots/"
SNAP_SHOT_NAME = "snap_demo"
SNAP_SHOT_NETWORK_NAME = "demo_netw"
HOST_VARS_DIR = "./snapshots/configs/"
FW_CHECKS = "./fw_checks.json"

def setup() -> None:
    """
    Set up the Batfish session and initialize the snapshot.
    """
    bf.host = "localhost"
    logger.info(f"Setting Batfish host to {bf.host}")
    load_questions()
    bf.set_network(SNAP_SHOT_NETWORK_NAME)
    bf.init_snapshot(SNAPSHOT_DIR, name=SNAP_SHOT_NAME, overwrite=True)


def check_acl_unreachable_lines(acl_name: str) -> None:
    """
    Check if an ACL has any unreachable lines.

    Args:
        acl_name: The name of the ACL to check.

    Raises:
        SystemExit: If unreachable lines are found in the ACL.
    """
    try:
        result = asserts.assert_filter_has_no_unreachable_lines(filters=acl_name)
        if not result:
            logger.error(f"Unreachable lines found in ACL {acl_name}")
            sys.exit(1)
        else:
            logger.info(f"No unreachable lines in ACL {acl_name}")
    except Exception as e:
        logger.error(f"Error checking ACL {acl_name}: {e}")
        sys.exit(1)


def check_acl_permits_flow(acl_name: str, ip_protocols: List[str], src_ip: str, dst_ip: str, dst_port: int) -> None:
    """
    Check if an ACL permits a specific source IP.

    Args:
        acl_name: The name of the ACL to check.
        ip_protocols: The list of IP protocols to match.
        src_ip: The source IP to match.
        dst_ip: The destination IP to match.
        dst_port: The destination port to match.

    Raises:
        SystemExit: If the ACL does not permit the source IP.
    """
    try:
        header_constraints = HeaderConstraints(ipProtocols=ip_protocols, srcIps=src_ip, dstIps=dst_ip, dstPorts=dst_port)
        result = asserts.assert_filter_permits(filters=acl_name, headers=header_constraints)
        if not result:
            logger.error(f"ACL {acl_name} does not permit {header_constraints}")
            sys.exit(1)
        else:
            logger.info(f"ACL {acl_name} permits source IP {header_constraints}")
    except Exception as e:
        logger.error(f"Error checking if ACL {acl_name} permits {header_constraints}: {e}")
        sys.exit(1)


def load_configuration(config_file: str) -> dict:
    """
    Load a configuration from a JSON file.

    Args:
        config_file: The path to the JSON configuration file.

    Returns:
        The loaded configuration as a dictionary.
    """
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON configuration file {config_file}.")
        sys.exit(1)


if __name__ == "__main__":
    setup() # Set up the Batfish session and initialize the snapshot.

    acl_names = set(bf.q.searchFilters().answer().frame().Filter_Name.tolist()) # Get the list of ACL names from the snapshot.

    custom_fw_checks = load_configuration(FW_CHECKS) # Load the firewall checks from the configuration file.

    for acl_name in acl_names:
        check_acl_unreachable_lines(acl_name)
        for check in custom_fw_checks:
            if re.match(check['acl_name_regex'], acl_name):
                check_acl_permits_flow(acl_name, check['ip_protocols'], check['src_ip'], check['dst_ip'], check['dst_port'])