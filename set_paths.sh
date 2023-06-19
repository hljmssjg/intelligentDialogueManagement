if [[ "$OSTYPE" == "msys" ]]; then
  # set env variables on windows, assuming GitBash shell
  echo Setting environment variables for GitBash on Windows:
  PYTHONPATH="C:\Users\Finn\Desktop\WoZ4U\pynaoqi-python2.7-2.5.7.1-win32-vs2013\lib";
  export PYTHONPATH
  echo $PYTHONPATH
else
  # set env variables on linux/mac
  echo Setting environment variables for Bash on Linux/Mac
  export PYTHONPATH=${PYTHONPATH}:/home/jiangeng/WoZ4U/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages
  export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/home/jiangeng/WoZ4U/pynaoqi-python2.7-2.5.7.1-linux64/lib
fi