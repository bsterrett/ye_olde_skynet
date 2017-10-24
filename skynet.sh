#!/bin/bash

python_virtual_environment="python_virtual_environment"
virtual_environment_activation="${python_virtual_environment}/bin/activate"
virtualized_pip="${python_virtual_environment}/bin/pip3"
virtualized_python="${python_virtual_environment}/bin/python3"
selenium_server_standalone_filename="selenium-server-standalone-3.6.0.jar"
selenium_server_standalone="bin/${selenium_server_standalone_filename}"
selenium_server_standalone_url="https://selenium-release.storage.googleapis.com/3.6/${selenium_server_standalone_filename}"

# SETUP PYTHON VIRTUAL ENVIRONMENT, IF NECESSARY
if [ ! -d "${python_virtual_environment}" ]; then
  if ! type "virtualenv" > /dev/null; then
    echo "The python virtual environment manager 'virtualenv' is required"
    exit 1
  fi

  echo "Setting up a new virtual environment in directory: ${python_virtual_environment}/"
  virtualenv --no-site-packages -p "python3.6" "${python_virtual_environment}"
fi

# LOAD PYTHON VIRTUAL ENVIRONMENT
eval "source ${virtual_environment_activation}"

# INSTALL MISSING DEPENDENCIES, IF NECESSARY
eval "${virtualized_pip} install -r \"requirements.txt\" 1>/dev/null"

# CHECK FOR SELENIUM SERVER STANDALONE EXECUTABLE
if [ ! -f "${selenium_server_standalone}" ]; then
  echo "Downloading a selenium server standalone executable: ${selenium_server_standalone_url}"
  curl "${selenium_server_standalone_url}" --output "${selenium_server_standalone}"
  chmod +x ${selenium_server_standalone}
fi

if ! type "geckodriver" > /dev/null; then
  echo "The WebDriver 'geckodriver' is necessary to interact with Firefox."
  echo "Please download the latest version for your system here:"
  echo "https://github.com/mozilla/geckodriver/releases/latest"
  exit 1
fi

# CHECK FOR LOGS DIRECTORY
if [ ! -d logs ]; then
  mkdir logs
fi

# RUN SKYNET EXECUTABLE
eval "${virtualized_python} \"skynet/main.py\""

# UNLOAD PYTHON VIRTUAL ENVIRONMENT (probably not necessary)
deactivate

exit 0
