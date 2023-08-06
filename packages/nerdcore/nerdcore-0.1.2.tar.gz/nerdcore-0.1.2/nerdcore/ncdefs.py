import os

VERSION = '0.1.2'

"""  CORE PATHS

This is a framework-level PATH definitions file.
It is separate from defs.py for usage in nerd-new, when there is no project ROOT_PATH.
It is also used anywhere else a framework-level path is needed.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  """

# NC PATH (root package)
NC_PATH = os.path.dirname(__file__)

# CM DEPLOYMENTS
NC_DEPLOYMENTS_PATH = os.path.join(NC_PATH, "deployments")
# CM TASKS
NC_TASKS_PATH = os.path.join(NC_PATH, "tasks")
# CM ABILITIES
NC_ABILITIES_PATH = os.path.join(NC_PATH, "abilities")
# CM COMMANDS
NC_COMMANDS_PATH = os.path.join(NC_PATH, "commands")
# CM CONFIG
NC_CONFIG_PATH = os.path.join(NC_PATH, "config")

# ENV CLASS
NC_ENV_CLASS_PATH = os.path.join(NC_CONFIG_PATH, "env_class.py")
# NERD CONFIG CLASS
NC_NERD_CONFIG_CLASS_PATH = os.path.join(NC_CONFIG_PATH, "nerd_config_class.py")
# THEME CONFIG
NC_THEME_CONFIG_PATH = os.path.join(NC_CONFIG_PATH, 'theme.py')

# HELP
NC_HELP_PATH = os.path.join(NC_PATH, "help")

# STOR CORE
NC_STOR_PATH = os.path.join(NC_PATH, "stor")
NC_STOR_TEMP_PATH = os.path.join(NC_STOR_PATH, "temp")
NC_STOR_NERD_PATH = os.path.join(NC_STOR_PATH, "nerd")
NC_STOR_DEFAULTS_PATH = os.path.join(NC_STOR_PATH, "defaults")

# DEFAULTS
NC_ENV_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, ".env.default")
NC_NERD_MANIFEST_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, "nerd-manifest.yaml")
NC_NERD_CONFIG_DEFAULTS_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, "nerd-config-defaults.yaml")
NC_CONTEXT_FILE_EXAMPLE_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, 'context-file.txt')
NC_DEFAULT_DEPLOYMENT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, 'DefaultDeployment.py')
NC_GITIGNORE_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, '.default-gitignore')
NC_README_DEFAULT_PATH = os.path.join(NC_STOR_DEFAULTS_PATH, 'DEFAULT-README.md')

# ENTITY EXAMPLES
NC_ENTITY_EXAMPLES_PATH = os.path.join(NC_STOR_PATH, "entity_examples")
NC_EXAMPLE_COMMAND_PATH = os.path.join(NC_ENTITY_EXAMPLES_PATH, "example-command.py")
NC_EXAMPLE_DEPLOYMENT_PATH = os.path.join(NC_ENTITY_EXAMPLES_PATH, "example-deployment.py")
