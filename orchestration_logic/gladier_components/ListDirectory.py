from gladier import GladierBaseTool, generate_flow_definition

def ls(**data):
    """Do an 'ls' on the filesystem, given a ``dir``"""
    import os
    return os.listdir(os.getcwd())

@generate_flow_definition
class FileSystemListCommand(GladierBaseTool):
    """List files on the filesystem"""
    compute_functions = [ls]

