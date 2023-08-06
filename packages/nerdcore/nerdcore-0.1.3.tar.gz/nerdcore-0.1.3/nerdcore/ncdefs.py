import os
from pkg_resources import resource_filename

VERSION = '0.1.3'

"""  CORE PATHS

This is a framework-level PATH definitions file.
It is separate from defs.py for usage in nerd-new, when there is no project ROOT_PATH.
It is also used anywhere else a framework-level path is needed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  """

# NC PATH (root package)
NC_PATH = os.path.dirname(__file__)

# CM DEPLOYMENTS
NC_DEPLOYMENTS_PATH = resource_filename('nerdcore', "deployments")
# CM TASKS
NC_TASKS_PATH = resource_filename('nerdcore', "tasks")
# CM ABILITIES
NC_ABILITIES_PATH = resource_filename('nerdcore', "abilities")
# CM COMMANDS
NC_COMMANDS_PATH = resource_filename('nerdcore', "commands")
# CM CONFIG
NC_CONFIG_PATH = resource_filename('nerdcore', "config")

# ENV CLASS
NC_ENV_CLASS_PATH = resource_filename('nerdcore', "config/env_class.py")
# NERD CONFIG CLASS
NC_NERD_CONFIG_CLASS_PATH = resource_filename('nerdcore', "config/nerd_config_class.py")
# THEME CONFIG
NC_THEME_CONFIG_PATH = resource_filename('nerdcore', 'config/theme.py')

# HELP
NC_HELP_PATH = resource_filename('nerdcore', "help")

# STOR CORE
NC_STOR_PATH = resource_filename('nerdcore', "stor")
NC_STOR_TEMP_PATH = resource_filename('nerdcore', "stor/temp")
NC_STOR_NERD_PATH = resource_filename('nerdcore', "stor/nerd")
NC_STOR_DEFAULTS_PATH = resource_filename('nerdcore', "stor/defaults")

# DEFAULTS
NC_ENV_DEFAULT_PATH = resource_filename('nerdcore', "stor/defaults/.env.default")
NC_NERD_MANIFEST_DEFAULT_PATH = resource_filename('nerdcore', "stor/defaults/nerd-manifest.yaml")
NC_NERD_CONFIG_DEFAULTS_DEFAULT_PATH = resource_filename('nerdcore', "stor/defaults/nerd-config-defaults.yaml")
NC_CONTEXT_FILE_EXAMPLE_PATH = resource_filename('nerdcore', 'stor/defaults/context-file.txt')
NC_DEFAULT_DEPLOYMENT_PATH = resource_filename('nerdcore', 'stor/defaults/DefaultDeployment.py')
NC_GITIGNORE_DEFAULT_PATH = resource_filename('nerdcore', 'stor/defaults/.default-gitignore')
NC_README_DEFAULT_PATH = resource_filename('nerdcore', 'stor/defaults/DEFAULT-README.md')

# ENTITY EXAMPLES
NC_ENTITY_EXAMPLES_PATH = resource_filename('nerdcore', "stor/entity_examples")
NC_EXAMPLE_COMMAND_PATH = resource_filename('nerdcore', "stor/entity_examples/example-command.py")
NC_EXAMPLE_DEPLOYMENT_PATH = resource_filename('nerdcore', "stor/entity_examples/example-deployment.py")
