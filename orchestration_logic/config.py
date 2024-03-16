import os 

# Get the full path of the current file
file_path = os.path.realpath(__file__)
localpath = os.path.dirname(file_path)

InputPath = "/input/"
OutputPath = "/output/"
TransferFile = "test.txt"


# Config file for access creds
CLIENT_ID = ""
CLIENT_SECRET = ""
SCOPE_STRING = ""

DataStoreUUID = "b782400e-3e59-412c-8f73-56cd0782301f"
Compute_DS_UUID = "d920d765-dda0-41cb-a30e-11f5a5f455a4"

CollectionIDs = [DataStoreUUID, 
                 Compute_DS_UUID]

ComputeUUID = "3dce26ee-10ed-47a8-a7c7-a6aa68004349"

# Config for the LPAP flow
flow_config = {
  'input': {
    'endpoints': {
      'DS_1_uuid': '',
      'DS_2_uuid': '',
      'LPAP_uuid': ''
    },
    'directory_paths': {
      'DS_1': '',
      'DS_2': '',
      'LPAP_input': '',
      'LPAP_output': ''
    }
  }
}