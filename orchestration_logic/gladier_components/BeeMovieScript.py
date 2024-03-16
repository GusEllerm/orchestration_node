from gladier import GladierBaseTool, generate_flow_definition

def GetScript(**data):
    """Grab the Bee Movie Script"""
    import requests
    import shutil

    # URL of the Bee Movie script
    url = "https://courses.cs.washington.edu/courses/cse163/20wi/files/lectures/L04/bee-movie.txt"
    # Send a HTTP request to the URL of the script
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
      # Write the script to a file
      with open('input/test.txt', 'w') as file:
        file.write(response.text)
      # Move the file to the output directory
      shutil.move('input/test.txt', 'output/test.txt')
    else:
      print("Failed to download the script.")
    

@generate_flow_definition
class GetBeeMovieScript(GladierBaseTool):
    """Get the Bee Movie Script"""
    compute_functions = [GetScript]

