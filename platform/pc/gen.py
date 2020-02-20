# Copyright (c) 2018 Viktor Vorobjov

import sys, os
path = "../../upy_main/tools/gen_tool"
gen_tool_path = os.path.abspath("{}/".format(path))
sys.path.append(gen_tool_path)

print(gen_tool_path)
from gen_tool import *

print("Gen libs")
path_ulib       = "../../upy_main/micropython-lib"
path_emu       = "../../upy_main/emu_lib"
path_core       = "../../upy_main/ucore"
path_app_mod    = "../../upy_main/umod"

work_path = "."

work_app_path   = "./app"
work_core_path  = "./core"
work_lib_path   = "./lib"
work_mod_path   = "./mod"

print("-- Path")
print(path_ulib)
print(work_path)
print(work_lib_path)

print("-- Start Gen Lib")


libs = (


# LIB PC

    # logging
    {
        "src_lib": path_ulib,
        "src_path": "logging/simple",
        "src": "logging.py",
        "dst_lib": work_lib_path,
        "dst_path": ""
    },

    # machine
    {
        "src_lib": path_emu,
        "src_path": "esp32/machine",
        "src": "__init__.py",
        "dst_lib": work_lib_path,
        "dst_path": "machine"
    },

    {
        "src_lib": path_emu,
        "src_path": "esp32/machine",
        "src": "emu_pin.py",
        "dst_lib": work_lib_path,
        "dst_path": "machine"
    },

    {
        "src_lib": path_emu,
        "src_path": "esp32/machine",
        "src": "emu_state.py",
        "dst_lib": work_lib_path,
        "dst_path": "machine"
    },


    # network
    {
        "src_lib": path_emu,
        "src_path": "esp32/network",
        "src": "__init__.py",
        "dst_lib": work_lib_path,
        "dst_path": "network"
    },

    {
        "src_lib": path_emu,
        "src_path": "esp32/network",
        "src": "emu_wlan.py",
        "dst_lib": work_lib_path,
        "dst_path": "network"
    },


#CORE

    # board
    {
        "src_lib": path_core,
        "src_path": "board/pc",
        "src": "platform.py",
        "dst_lib": work_core_path,
        "dst_path": ""
    },

    # loader
    {
        "src_lib": path_core,
        "src_path": "",
        "src": "loader.py",
        "dst_lib": work_core_path,
        "dst_path": ""
    },

    # asyn
    {
        "src_lib": path_core,
        "src_path": "asyn",
        "src": "asyn.py",
        "dst_lib": work_core_path,
        "dst_path": "asyn"
     },

    # db
    {
        "src_lib": path_core,
        "src_path": "db",
        "src": "filedb.py",
        "dst_lib": work_core_path,
        "dst_path": "db"
    },

    # mbus
    {
        "src_lib": path_core,
        "src_path": "mbus",
        "src": "mbus.py",
        "dst_lib": work_core_path,
        "dst_path": "mbus"
    },

    # umod
    {
        "src_lib": path_core,
        "src_path": "umod",
        "src": "board.py",
        "dst_lib": work_core_path,
        "dst_path": "umod"
    },

    {
        "src_lib": path_core,
        "src_path": "umod",
        "src": "table.py",
        "dst_lib": work_core_path,
        "dst_path": "umod"
    },

    {
        "src_lib": path_core,
        "src_path": "umod",
        "src": "umod.py",
        "dst_lib": work_core_path,
        "dst_path": "umod"
    },

#APP

    # FTP app
    {
        "src_lib": path_app_mod,
        "src_path": "ftp/app",
        "src": "ftp_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

        # FTP mod
    {
        "src_lib": path_app_mod,
        "src_path": "ftp/mod",
        "src": "ftp.py",
        "dst_lib": work_mod_path,
        "dst_path": "ftp"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "ftp/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "ftp"
    },


    # TELNET app
    {
        "src_lib": path_app_mod,
        "src_path": "telnet/app",
        "src": "telnet_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

    # TELNET mod
    {
        "src_lib": path_app_mod,
        "src_path": "telnet/mod",
        "src": "telnet.py",
        "dst_lib": work_mod_path,
        "dst_path": "telnet"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "telnet/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "telnet"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "telnet/mod",
        "src": "telnetio.py",
        "dst_lib": work_mod_path,
        "dst_path": "telnet"
    },

    # HTTP app
    {
        "src_lib": path_app_mod,
        "src_path": "http/app",
        "src": "http_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

        # HTTP mod
    {
        "src_lib": path_app_mod,
        "src_path": "http/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "http"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "http/mod",
        "src": "route_rpc.py",
        "dst_lib": work_mod_path,
        "dst_path": "http"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "http/mod",
        "src": "http.py",
        "dst_lib": work_mod_path,
        "dst_path": "http"
    },


    # NET app

    {
        "src_lib": path_app_mod,
        "src_path": "net/app",
        "src": "net_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

        # NET mod
    {
        "src_lib": path_app_mod,
        "src_path": "net/mod",
        "src": "actions.py",
        "dst_lib": work_mod_path,
        "dst_path": "net"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "net/mod/esp32",
        "src": "wifi.py",
        "dst_lib": work_mod_path,
        "dst_path": "net"
    },

    # MQTT app
    {
        "src_lib": path_app_mod,
        "src_path": "mqtt/app",
        "src": "mqtt_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

    # MQTT mod
    {
        "src_lib": path_app_mod,
        "src_path": "mqtt/mod",
        "src": "mqtt.py",
        "dst_lib": work_mod_path,
        "dst_path": "mqtt"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "mqtt/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "mqtt"
    },


    {
        "src_lib": path_app_mod,
        "src_path": "mqtt/mod",
        "src": "message.py",
        "dst_lib": work_mod_path,
        "dst_path": "mqtt"
    },

    # PIN

    # PIN app
    {
        "src_lib": path_app_mod,
        "src_path": "pin/app",
        "src": "pin_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

    # PIN mod
    {
        "src_lib": path_app_mod,
        "src_path": "pin/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "pin"
    },

    # PUSH

    # PUSH app
    {
        "src_lib": path_app_mod,
        "src_path": "push/app",
        "src": "push_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

    # PUSH mod
    {
        "src_lib": path_app_mod,
        "src_path": "push/mod",
        "src": "push.py",
        "dst_lib": work_mod_path,
        "dst_path": "push"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "push/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "push"
    },

    # RELAY

    # RELAY app
    {
        "src_lib": path_app_mod,
        "src_path": "relay/app",
        "src": "relay_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

    # RELAY mod
    {
        "src_lib": path_app_mod,
        "src_path": "relay/mod",
        "src": "relay.py",
        "dst_lib": work_mod_path,
        "dst_path": "relay"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "relay/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "relay"
    },

    # Control

    # Control app
    {
        "src_lib": path_app_mod,
        "src_path": "control/app",
        "src": "control_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

    # Control mod

    {
        "src_lib": path_app_mod,
        "src_path": "control/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "control"
    },

# PWM

    # PWM app
    {
        "src_lib": path_app_mod,
        "src_path": "pwm/app",
        "src": "pwm_mod.py",
        "dst_lib": work_app_path,
        "dst_path": ""
    },

    # PWM mod
    {
        "src_lib": path_app_mod,
        "src_path": "pwm/mod",
        "src": "pwm.py",
        "dst_lib": work_mod_path,
        "dst_path": "pwm"
    },

    {
        "src_lib": path_app_mod,
        "src_path": "pwm/mod",
        "src": "runner.py",
        "dst_lib": work_mod_path,
        "dst_path": "pwm"
    },



)


gen_libs(libs)

