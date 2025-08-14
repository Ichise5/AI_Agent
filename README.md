# AI_Agent

## About
A Bootdev AI Agent project to learn how make a program to utilize AI as a coding assitance.

## Security
It has been emphasized that this project does not contain all the security features it could (I added even more dangerous feature to the combo - delete file).
Although, system prompt emphasized that sensitive and personal information are not supposed to be handled unless specified... Well... One can not be sure enough...

## Features
Working folder is a parameter that is set outside of the functions and is supposed to be stay (hopefully) outside of the scope of working of the Agent.
- List files and directories in the working folder
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Format the code using Black frameworks and then lint it using Flake8 framework
- Delete files

## Dependencies
- uv
- black
- flake8
- google-genai
- python-dotenv
