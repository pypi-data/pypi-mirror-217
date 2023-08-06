from prompts import plan, specify_filePaths, generate_code
from utils import generate_folder, writeFile
import os
import sys

def main(app_prompt, generateFolder = "generated", debug=False):
  # create generateFolder folder if doesnt exist
  generate_folder(generateFolder)

  # plan sharedDeps
  if debug: print('--------sharedDeps---------')
  sharedDeps = plan(app_prompt)
  if debug: print(sharedDeps)
  writeFile(f"{generateFolder}/shared_deps.md", sharedDeps)
  if debug: print('--------sharedDeps---------')
  
  # specify filePaths
  if debug: print('--------specify_filePaths---------')
  filePaths = specify_filePaths(app_prompt, sharedDeps)
  if debug: print(filePaths)
  if debug: print('--------filePaths---------')

  # loop through filePaths array and generate code for each file
  for filePath in filePaths:
    filePath = f"{generateFolder}/{filePath}" # just append prefix
    if debug: print(f'--------generate_code: {filePath} ---------')
    code = generate_code(app_prompt, sharedDeps, filePath)
    if debug: print(code)
    if debug: print(f'--------generate_code: {filePath} ---------')
    # create file with code content
    writeFile(filePath, code)


# for local testing
if __name__ == "__main__":
  app_prompt = sys.argv[1] if len(sys.argv) >= 2 else """
  a simple JavaScript/HTML/CSS app that plays the game of Snake, using keyboard up/down/left/right controls.
  """
  print(app_prompt)
  generateFolder = "generated"

  main(app_prompt, generateFolder, debug=True)