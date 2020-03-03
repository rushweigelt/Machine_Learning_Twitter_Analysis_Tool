"""
The experiment platform is a tool for automatically and repeatedly training
machine learning models against various datasets. All model training results
and artifacts are saved to a central MLFlow server.
"""
import os

try:
    PARALLELISM = int(os.getenv("PARALLELISM", "4"))
except ValueError:
    print(
        "Value of PARALLELISM env var was unable to be cast to int. Using default value of 4."
    )
    PARALLELISM = 4
