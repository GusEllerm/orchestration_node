"""
This file contains a single LivePublication Action Provider flow using Gladier & Globus interfaces. 
It serves as an experimental testbench for the LivePublication CLI.
"""
import json
import os

from gladier import GladierBaseClient, generate_flow_definition
from globus_sdk.scopes import GCSCollectionScopeBuilder, TransferScopes
from pprint import pprint

# Import config variables & custom tools
from .logger_config import logger
from .config import DataStoreUUID, ComputeUUID, CollectionIDs, Compute_DS_UUID, InputPath, OutputPath, TransferFile
from .gladier_components.BeeMovieScript import GetBeeMovieScript
from .gladier_components.ListDirectory import FileSystemListCommand

def run_flow():
    """
    This function runs the LivePublication Action Provider flow using Gladier & Globus interfaces.
    """
    @staticmethod
    @generate_flow_definition
    class Example_Flow(GladierBaseClient):
        """
        Note the order of the tools - this defines the order of the flow.
        Also, note how this comment is included within the WEP as a comment.

        These components (here called tools) are disconnected descriptions of the 
        actions which gladier will stitch together into a flow.
        When instantiating the prospective provenance, these components could be
        used as the software components of each action.
        """
        gladier_tools = [
            "gladier_tools.globus.Transfer:ToCompute",
            FileSystemListCommand,
            GetBeeMovieScript,
            "gladier_tools.globus.Transfer:FromCompute",
            # FileSystemListCommand
            # "gladier_tools.posix.Tar"
        ]

    flow_input = {
        "input": {
            # Input vars for transfer 1 (FromSource)
            "to_compute_transfer_source_endpoint_id": DataStoreUUID,
            "to_compute_transfer_destination_endpoint_id": Compute_DS_UUID,
            "to_compute_transfer_source_path": os.path.join(OutputPath, TransferFile),
            "to_compute_transfer_destination_path": os.path.join(InputPath, TransferFile),
            "to_compute_transfer_recursive": False,
            # Input vars for transfer 2 (ToDestination)
            "from_compute_transfer_source_endpoint_id": Compute_DS_UUID,
            "from_compute_transfer_destination_endpoint_id": DataStoreUUID,
            "from_compute_transfer_source_path": os.path.join(OutputPath, TransferFile),
            "from_compute_transfer_destination_path": os.path.join(InputPath, TransferFile),
            "from_compute_transfer_recursive": False,
            # Compute Endpoint for interfacing with the compute endpoint
            "compute_endpoint": ComputeUUID
        }
    }

    example_flow_client = Example_Flow()

    # Because we are using Globus Connect Server's for Mapped Collections,
    # we need to add each collection endpoint's scope to the flow's input.
    # TODO: This is currently only semi working, Globus still requires input from the user.
    GCS_Scopes = []
    for collection_id in CollectionIDs:
        scope_builder = GCSCollectionScopeBuilder(collection_id)
        scope_string = scope_builder.make_mutable("data_access", optional=True).scope_string
        GCS_Scopes.append(scope_string)
    logger.debug(f"Adding scopes: {GCS_Scopes}")
    example_flow_client.login_manager.add_requirements(GCS_Scopes + example_flow_client.scopes)
    
    logger.debug(json.dumps(example_flow_client.get_flow_definition(), indent=2))
    flow = example_flow_client.run_flow(
        flow_input=flow_input,
        label="Simple four step with Compute and Connect Servers",
    )

    # If you want to wait on the output, 
    # you can use the following code:

    # action_id = flow['action_id']
    # example_flow_client.progress(action_id)
    # pprint(flow.result(action_id))