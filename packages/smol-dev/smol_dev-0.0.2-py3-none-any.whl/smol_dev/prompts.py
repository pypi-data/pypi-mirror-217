import openai
from typing import List
from openai_function_call import openai_function
import re

# openaimodel = "gpt-3.5-turbo-0613"
openaimodel = "gpt-4-0613"

smol_dev_system_prompt = """
You are an AI developer who is trying to write a program that will generate code for the user based on their intent.
"""




@openai_function
def filePaths(filesToEdit: List[str]) -> List[str]:
    """Takes a list of filepaths relative to the current directory and returns a list of filepaths that need to be edited."""
    print('filesToEdit', filesToEdit)
    return filesToEdit


def specify_filePaths(prompt: str, sharedDependencyManifest: str):
  completion = openai.ChatCompletion.create(
          model=openaimodel,
          temperature=0.7,
          functions=[filePaths.openai_schema],
          function_call={ "name": "filePaths" },
          messages=[
              {
                  "role": "system",
                  "content": f"""{smol_dev_system_prompt}
          
      When given their intent, create a complete, exhaustive list of filepaths that the user would write to make the program.
      
      only list the filepaths you would write, and return them as a python list of strings. 
      do not add any other explanation, only return a python list of strings.
                  """,
              },
              {
                  "role": "user",
                  "content": f""" I want a: {prompt} """,
              },
              {
                  "role": "user",
                  "content": f""" The shared dependencies we have agreed on are: {sharedDependencyManifest} """,
              },
          ],
      )
  result = filePaths.from_response(completion)
  return result
  

def passthrough(prompt: str):
  print('passthrough', prompt)
  return prompt

# def plan(prompt: str, filePaths: List[str]):
def plan(prompt: str):
  completion = openai.ChatCompletion.create(
          model=openaimodel,
          temperature=0.7,
          messages=[
              {
                  "role": "system",
                  "content": f"""{smol_dev_system_prompt}
      
  In response to the user's prompt, 
  Please name and briefly describe the structure of the app we will generate, including, for each file we are generating, what variables they export, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.
                  """,
  # Exclusively focus on the names of the shared dependencies, and do not add any other explanation.
              },
              # {
              #     "role": "user",
              #     "content": f""" the files we have decided to generate are: {filePaths} """,
              # },
              {
                  "role": "user",
                  "content": f""" the app prompt is: {prompt} """,
              },
          ],
      )
  # result = sharedDeps.from_response(completion)
  # return result
  return completion.choices[0].message.content


#####
# TODO: explore pydantic models for export to morph/rift
#####
# from pydantic import BaseModel, Field # probably doesn't compile

# class CodeFile(BaseModel):
#     file_name: str = Field("Name of the file")
#     file_contents: str = Field("Contents of the file. Must compile correctly")
    
# class SmolDeveloperManifest(BaseModel):
#     md_contents = Field("flat md file which specifies the directory tree of the app we are generating")

# # we want to compute this result incrementally through a chain of thought, i.e.
# # first, synthesize the manifest
# # then synthesize partial codefiles with filenames and filepaths
# # then for all codefiles synthesize content
# class SmolDeveloperResult(BaseModel):
#     manifest: SmolDeveloperManifest
#     code_files: List[CodeFile]

@openai_function
def validCodeFile(codeFile: str) -> str:
    """Receives a string of valid code and, after checking for code blocks, returns a string of code that is valid."""
    # pattern = r"```[\w\s]*\n([\s\S]*?)```" # original regex for code blocks anywhere in the string
    print('----codeFile', codeFile)
    pattern = r"^\s*```[ws]*\n([sS]*?)```" # codeblocks at start of the string, less eager
    code_blocks = re.findall(pattern, codeFile, re.MULTILINE)
    return code_blocks[0] if code_blocks else codeFile

def generate_code(prompt: str, sharedDependencyManifest: str, currentFile: str):
  completion = openai.ChatCompletion.create(
          model=openaimodel,
          temperature=0.7,
          functions=[validCodeFile.openai_schema],
          function_call={ "name": "validCodeFile" },
          messages=[
              {
                  "role": "system",
                  "content": f"""{smol_dev_system_prompt}
      
  In response to the user's prompt, 
  Please name and briefly describe the structure of the app we will generate, including, for each file we are generating, what variables they export, data schemas, id names of every DOM elements that javascript functions will use, message names, and function names.

  We have broken up the program into per-file generation. 
  Now your job is to generate only the code for the file: {currentFile} 
  
  only write valid code for the given filepath and file type, and return only the code.
  do not add any other explanation, only return valid code for that file type.
                  """,
              },
              {
                  "role": "user",
                  "content": f""" the plan we have agreed on is: {sharedDependencyManifest} """,
              },
              {
                  "role": "user",
                  "content": f""" the app prompt is: {prompt} """,
              },
              {
                  "role": "user",
                  "content": f"""
    Make sure to have consistent filenames if you reference other files we are also generating.
    
    Remember that you must obey 3 things: 
       - you are generating code for the file {currentFile}
       - do not stray from the names of the files and the shared dependencies we have decided on
       - MOST IMPORTANT OF ALL - every line of code you generate must be valid code. Do not include code fences in your response, for example
    
    Bad response:
    ```javascript 
    console.log("hello world")
    ```
    
    Good response:
    console.log("hello world")
    
    Begin generating the code now.

    """,
              },
          ],
      )
  codeFile = validCodeFile.from_response(completion)
  return codeFile
#   print('xxxxxcodeFile', codeFile)
#   pattern = r"^\s*```[ws]*\n([sS]*?)```" # codeblocks at start of the string, less eager
#   code_blocks = re.findall(pattern, codeFile, re.MULTILINE)
#   return code_blocks[0] if code_blocks[0] is not None else codeFile
# #   return result
# #   return completion.choices[0].message.content