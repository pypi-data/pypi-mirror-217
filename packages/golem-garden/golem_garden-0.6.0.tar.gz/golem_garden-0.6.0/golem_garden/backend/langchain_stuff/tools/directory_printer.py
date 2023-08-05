import pathlib
from pathlib import Path

from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import BaseTool
from pydantic import Field


EXCLUDED_DIRECTORIES = [".git",
                        ".idea",
                        "venv",
                        "utilities",
                        "tests",
                        "docs",
                        "data",
                        "golem_garden.egg-info",
                        ]
INCLUDED_FILE_EXTENSIONS = [".py",
                            ".md", ]

class DirectoryWalker(BaseTool):
    name = "query_webpage"
    description = "A class to walk through a directory and print its structure."
    text_splitter: RecursiveCharacterTextSplitter = Field(default_factory=_get_text_splitter)
    qa_chain: BaseCombineDocumentsChain



    def __init__(self,
                 root_dir: str,
                 excluded_directories: list = EXCLUDED_DIRECTORIES,
                 included_file_extensions: list = INCLUDED_FILE_EXTENSIONS ):
        """
        Initialize the DirectoryWalker.

        Args:
            root_dir (str): The root directory to start walking from.
        """
        self.root_dir = Path(root_dir)
        self._excluded_directories = excluded_directories
        self._included_file_extensions = included_file_extensions
        self._excluded_files = [".DS_Store"]
        self._excluded_file_extensions = [".pyc"]

    def walk(self, current_dir: Path, indent_level: int = 0):
        """
        Recursively walk through a directory and print its structure.

        Args:
            current_dir (Path): The current directory to walk through.
            indent_level (int, optional): The indentation level for printing. Defaults to 0.
        """
        for item in current_dir.iterdir():

            if item.is_file():
                if item.name in self._excluded_files:
                    continue
                if item.suffix in self._excluded_file_extensions:
                    continue
                if item.name in self._included_file_extensions:
                    print("  " * indent_level, "├──", item.name)
                    continue
                print("  " * indent_level, item.name)
            if item.is_dir():
                print("  " * indent_level, "├──", item.name + "/")
            if item.is_dir():
                if item.name in self._excluded_directories:
                    continue
                print("  " * indent_level, "└──")
                self.walk(item, indent_level + 1)

    def print_structure(self):
        """
        Print the folder structure and files in the root directory.
        """
        self.walk(self.root_dir)


if __name__ == "__main__":
    # root_directory = input("Enter the root directory: ")
    # root_directory = r"C:\Users\jonma\github_repos\jonmatthis\golem_garden"
    root_directory = r"C:\Users\jonma\github_repos\jonmatthis\Alpaca-Turbo"


    print(f"Printing the structure of {root_directory}...")
    walker = DirectoryWalker(root_dir=root_directory,
                             excluded_directories=excluded_directories,
                             included_file_extensions=included_file_extensions
                             )
    walker.print_structure()
