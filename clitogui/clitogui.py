#!/usr/bin/python3
"""
Decorator file.
Everything start from here.
"""

##########
# IMPORT #
##########
import argparse
import sys
import tkinter as tk

from argparse import ArgumentParser
from collections import defaultdict

from .gui import Interface

#############
# DECORATOR #
#############
def clitogui(parser_function):
    """
    To add on the parser function.
    Extract arguments from the parser and send them to the GUI constructor
    (cf gui.py).
    """

    # ARGPARSE TO GUI
    def argparse_to_gui(payload):
        """
        Function to setup the build of the GUI, from an argparse parser.
        """

        def argparse_args_extractor(parser):
            """
            Generation of widgets based on the parser.
            Input: Parser function
            Output: Generator of arguments
            """
            # We don't want to send Help and Version action
            for action in tuple(parser._actions):
                if type(action) != argparse._HelpAction and\
                type(action) != argparse._VersionAction:
                    yield action

        def argparse_gui_builder(self):
            """
            Generate the GUI, save arguments back from it, and build the CLI
            for the parser.
            """
            root = tk.Tk()
            # Use of Interface object from gui.py
            gui = Interface(root, argparse_args_extractor(self))
            root.mainloop()
            return self.old_parse_args(gui.out_args)

        def argparse_alterator(*args, **kwargs):
            """
            Change ArgParse.parse_args function.
            """
            # Saving the old argument parser for later
            ArgumentParser.old_parse_args = ArgumentParser.parse_args
            # Replace the parse_args function by our own, to allow call from
            # the user script
            ArgumentParser.parse_args = argparse_gui_builder
            return payload(*args, **kwargs)

        argparse_alterator.__name__ = payload.__name__
        return argparse_alterator

    # Allow to ignore clitogui in the CLI, for testing purpose
    if "--cli" in sys.argv:
        sys.argv.remove("--cli")
        return parser_function
    else:
        return argparse_to_gui(parser_function)
