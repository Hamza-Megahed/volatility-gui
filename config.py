#!/usr/bin/python3

#===============================================================================
#  Name        : config.py
#  Author      : Hamza
#  Version     : v1.0
#  Copyright   : Your copyright notice
#  Description : build profile and set config parameters to the main script
#===============================================================================

import os

config = {
    "python_bin" : "python", #name of python 2 binary 
    "volatility_bin_loc" : "/home/test/volatility-2.6/volatility-master/vol.py", #volatility binart absolute path
    "saved_config" : ".conf/" #config dirctory to be created 
    }

conf_dir = os.path.join(os.path.dirname(__file__), config["saved_config"])
profile_file = conf_dir+"profiles"


if __name__ == "__main__":

    os.makedirs(conf_dir, exist_ok=True) # create config file 
    # create profiles list
    os.system(config["python_bin"] + " " + config["volatility_bin_loc"] + " --info | grep 'A Profile' | cut -f1 -d '-' > " + profile_file)
