from nerdcore.ncdefs import NC_COMMANDS_PATH, NC_DEPLOYMENTS_PATH
from nerdcore.base_entitiies.command_class import Command
from nerdcore.utils.nerd.theme_functions import print_tree
from nerdcore.defs import COMMANDS_PATH, DEPLOYMENTS_PATH


class List(Command):
    named_arg_keys = ['all']
    all: bool = False

    def run(self):

        print_tree(NC_COMMANDS_PATH, exclude_file_starts=['.', '_'],
                   title="📁  Commands - Run CLI commands", incl_prefix=False)
        print_tree(COMMANDS_PATH, exclude_file_starts=['.', '_'], incl_prefix=False)

        if self.all:
            print_tree(NC_DEPLOYMENTS_PATH, exclude_file_starts=['.', '_'],
                       title="🤖  Deployments - Run deployments with nerd configs", incl_prefix=False)
            print_tree(DEPLOYMENTS_PATH, exclude_file_starts=['.', '_'], incl_prefix=False)
