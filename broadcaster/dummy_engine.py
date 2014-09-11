import ConfigParser
import importlib
import os.path
import glob
from os.path import basename, splitext, expanduser, sep
import os

__plugins_dir__ = "./broadcaster/plugins"
__private_home__=expanduser("~")+sep+".Broadcaster"
__pkg__="broadcaster.plugins"
__cfgfile__=__private_home__+sep+"conf.ini"
__conf__=None
__all_chnl__=None
__ui__=None
__debug_mode__=False

class Engine(object):
    """class engine for plugins"""
    
    def __init__(self, plugin):
        """identifying plugin and setting-up conf"""
        self.section=plugin
	self.UI=__ui__

    def get_attrib(self, option):
        """return attribute from conf"""
 	if __conf__.has_option(self.section,option):
            value=__conf__.get(self.section,option)
        else:
            value=""
        return value

    def set_attrib(self, option, value):
        """stores option-value pair to the conf"""
        global __conf__
        if not __conf__.has_section(self.section):
            __conf__.add_section(self.section)
        __conf__.set(self.section, option, value)

    def prompt_user(self, msg, type=None, debug=False):
        """prompts user with msg and return the input from user"""
        if debug and (not __debug_mode__):
            return None
        else:
            return self.UI.prompt(msg, type)
        

def broadcast(msg, chnl_list, mode, ui):
    global __ui__, __all_chnl__, __debug_mode__, __conf__
    __ui__=ui
    __debug_mode__=mode
    dict={}
    __all_chnl__=get_chnls()
    __conf__=get_conf()
    for chnl in chnl_list:
        if has_channel(chnl):
            plug=load_plugin(chnl, msg)
            try:
                plug.post()
                dict[chnl]="Successful"
            except Exception as x:
                dict[chnl]="Failed ::-> "+x.message
        else:
            dict[chnl]="Failed: Plugin not found..\n To add new plugin, insert plugin file to broadcaster/plugins"
    set_conf(__conf__)
    return dict

def get_chnls():
    plugins = []
    plugin_files = glob.glob("{}/*.py".format(__plugins_dir__))
    for plugin_file in plugin_files:
        if plugin_file.endswith("__init__.py"):
            continue
        name, ext = splitext(basename(plugin_file))
        plugins.append(name)
    return plugins

def has_channel(chnl):
    if chnl in __all_chnl__:
        return True
    else:
        return False

def load_plugin(chnl, msg):
    engine=Engine(chnl)
    mod=importlib.import_module("."+chnl, __pkg__)
    return getattr(mod,chnl)(engine, msg)

def get_conf():
    conf=ConfigParser.ConfigParser()
    conf.read(__cfgfile__)
    return conf

def set_conf(conf):
    try:
        if not os.path.isfile(__cfgfile__):
            if not os.path.exists(__private_home__):
                os.makedirs(__private_home__)
        conf_file=open(__cfgfile__,"w")
        conf.write(conf_file)
        conf.close()
        return True
    except Exception:
        return False

def reset_plugin(chnls):
    try:
        dict={}
        if os.path.isfile(__cfgfile__):
            conf=ConfigParser.ConfigParser()
            conf.read(__cfgfile__)
            for chnl in chnls:
                if conf.has_section(chnl):
                    conf.remove_section(chnl)
                    dict[chnl]="reset"
                else:
                    dict[chnl]="no data to reset"
            conf.write(open(__cfgfile__,"w"))
        else:
            dict["all-channel"]="no data to reset"
        return dict
    except Exception:
        return {"all-channel":"reset failed"}
                
