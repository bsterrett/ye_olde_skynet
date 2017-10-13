#!/bin/bash

python_virtual_environment="python_virtual_environment"
virtual_environment_activation="${python_virtual_environment}/bin/activate"
virtualized_pip="${python_virtual_environment}/bin/pip3"
virtualized_python="${python_virtual_environment}/bin/python3"

# SETUP PYTHON VIRTUAL ENVIRONMENT, IF NECESSARY
if [ ! -d "${python_virtual_environment}" ]; then
  if ! type "pip" > /dev/null; then
    echo "The python package manager 'pip' is required to manage dependencies"
    exit 1
  fi

  if ! type "virtualenv" > /dev/null; then
    echo "The python virtual environment manager 'virtualenv' is required"
    exit 1
  fi

  echo "Setting up a new virtual environment in directory: ${python_virtual_environment}/"
  virtualenv --no-site-packages -p "python3" "${python_virtual_environment}"
fi

# LOAD PYTHON VIRTUAL ENVIRONMENT
eval "source ${virtual_environment_activation}"

# INSTALL MISSING DEPENDENCIES, IF NECESSARY
eval "${virtualized_pip} install -r \"requirements.txt\" 1>/dev/null"

# RUN SKYNET EXECUTABLE
eval "${virtualized_python} \"skynet/main.py\""

# UNLOAD PYTHON VIRTUAL ENVIRONMENT (probably not necessary)
deactivate

exit 0
