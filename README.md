# OU-Final-Project
This is the open-source version of the repository I used for the code (and assignments omitted from here) in the TM470 module for my Bachelor's degree from Open University. 
The purpose of repo is to give the grader and the public access to the software developed during the module. Please note that this repository does not contain the original commit history, due to time constraints and the fact that the repository was private for the duration of the module as it contained information that was not to be shared with the public, e.g., assignments drafts, etc.

However, this repo contains the full code, and a commit history that should give indications about the software development process. The old GitHub issues are not linked to this repo, however, the final development is meant to happen in this repo, and any new issues will be linked to this repo.

## Goals

This program aims to help me with the research project I conducted as my final project. The research centers around the main hypothesis H1:

    Live arbitrage opportunities are identifiable in multiple zero-sum sports.

This hypothesis was drafted based on the current literature. The software aims to validate or invalidate this hypothesis by identifying live arbitrage opportunities (AOs) in multiple zero-sum sports utilizing `https.oddsportal.com` as the primary data source to scrape, clean, transform, and analyze near-real-time data (and metadata).
The software aims to identify AOs in the following sports:
- tennis
- table tennis
- basketball

This list might be extended in the future if time permits it. This extendability is linked to the second objective of the research, which is as follows:

    # Development and Evaluation of a Technological Solution
    
    This project seeks to develop an open-source software tool that can identify 
    arbitrage opportunities in near-real-time. The tool will collect and analyze data
    from online sources, utilizing appropriate techniques. The data includes a broader
    set of sports compared to most existing literature, thus providing a comprehensive
    view of the global sports betting market. The software is developed with best
    practices to achieve an efficient, reliable, and easy-to-extend solution. 
    The application will include a data storage solution to ensure the reproducibility of
    the results and transparency of the data utilized. The tool's development will 
    demonstrate the practical application of theoretical concepts discussed in the
    literature and provide a platform for future research and development in this field,
    as outlined in the introduction.

    (TMA03, Piirtola 2023) 

This repo will contain the code for the live arbitrage identificator. It also contains a set of JupyterNotebooks in which other relevant research questions are explored including the nature and context in which these possible AOs occur, e.g., do sets of bookmakers from local or global markets offer AOs, etc.

## Installation and Usage

- TODO: Write a simple guide on how to install and use the software.

## Architecture

- TODO: Write a simple architectural guide on how the software is structured.

## Docstrings

The general format that the docstrings should follow is as follows:

```python

def some_function(x: str, y: int) -> str:
    """
    This text should be a brief description of the function, and what it does and possibly why it does it.

    Args:
        x: This is the first argument, and should be a string and this text explains what it is.
        y: This is the second argument, and should be an integer and this text explains what it is.

    Returns:
        str: This is the return value, and should be a string and this text explains what it is.
    """
    ...

class SomeClass:
    """
    This is the class description, and should be a brief description of the class, and what it does and possibly why it does it.
    
    This section is not mandatory, but if the description includes details relevant to the class but not to the init method, then it should be included here.
    """

    def __init__(self, attr1: int, attr2: str):
        """
        This text should be a brief description of the init method if needed
        """
        ...
        
    def some_method(self, attr1: int, attr2: str) -> str:
        """
        Similar method description as in the function docstring.
        """
        ...

    def _private_method(self, attr1: int, attr2: str) -> str:
        """
        Similar as above, however, should note why the function is a private method if this is the case.
        """
        ...
