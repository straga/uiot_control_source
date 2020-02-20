
_name_board = "default"


def push_board(umod):

    board_cfg = {
        "name":"default",
        "board":"PC_DEV_01",
        "hostname":"dev32.local",
        "uid":"2132323213",
        "client":"dev/pc_dev",
    }

    # umod.data_load("board_cfg",
    #                name="default",
    #                board="PC_DEV_01",
    #                hostname="dev32.local",
    #                uid="2132323213",
    #                client="dev/pc_dev",
    #                init="0"
    #                )

    # umod.data_load("board_mod", name="net",         active=1, status="", seq=1)
    # umod.data_load("board_mod", name="http",        active=1, status="", seq=2)
    # umod.data_load("board_mod", name="ftp",         active=0, status="", seq=3)
    # umod.data_load("board_mod", name="telnet",      active=0, status="", seq=4)
    # umod.data_load("board_mod", name="mqtt",        active=1, status="", seq=5)
    # umod.data_load("board_mod", name="pin",         active=1, status="", seq=6)
    # umod.data_load("board_mod", name="push",        active=1, status="", seq=7)
    # umod.data_load("board_mod", name="relay",       active=1, status="", seq=8)
    # umod.data_load("board_mod", name="control",     active=1, status="", seq=9)
    # umod.data_load("board_mod", name="pwm",         active=1, status="", seq=10)
    # umod.data_load("board_mod", name="ota",         active=1, status="", seq=11)
    # umod.data_load("board_mod", name="ota_server",  active=1, status="", seq=12)
    # umod.data_load("board_mod", name="web",         active=1, status="", seq=13)
    # umod.data_load("board_mod", name="i2c",         active=1, status="", seq=14)



def push_data(umod):
    pass


    # # STA
    # umod.data_load("cfg_wifi_sta",
    #                name="demosta",
    #                ssid="demosta",
    #                passwd="demosta",
    #                active=1
    #                )
    #
    # umod.data_load("cfg_wifi_sta",
    #                name="demosta2",
    #                ssid="demosta2",
    #                passwd="demosta2",
    #                active= 1
    #                )
    #
    # umod.data_load("cfg_wifi_sta",
    #                name="demosta2",
    #                ssid="demosta2",
    #                passwd="demosta2",
    #                active= 0
    #                )
    #
    #
    #
    # umod.data_load("cfg_wifi_sta",
    #                name="demosta2",
    #                ssid="demosta2",
    #                passwd="demosta2"
    #                )
    #
    # # AP
    # umod.data_load("cfg_wifi_ap",
    #                 name="default",
    #                 essid="esp32_dev",
    #                 channel=11,
    #                 hidden="false",
    #                 password="devwifidev",
    #                 authmode=3,
    #
    #                )
    #
    #
    #
    # # FTP
    # umod.data_load("cfg_ftp",
    #                name="default",
    #                ip="",
    #                port=25,
    #                dport=26
    #                )
    #
    # # MQTT
    # umod.data_load("cfg_mqtt",
    #                name="local_1",
    #                type="default",
    #                ip="192.168.100.235",
    #                port=1883
    #                )
    #
    # umod.data_load("cfg_mqtt",
    #                name="local_2",
    #                ip="192.168.197.128",
    #                port=1883
    #                )
    #
    # umod.data_load("cfg_mqtt",
    #                name="local_3",
    #                ip="192.168.254.1",
    #                port=1883
    #                )
    #
    #
    # # PIN
    # umod.data_load("board_pin", name="led_status",          name_pin="21",  psy_pin=21)
    # umod.data_load("board_pin", name="relay_1",             name_pin="22",  psy_pin=22)
    # umod.data_load("board_pin", name="btn_touch",           name_pin="19",  psy_pin=19)
    # umod.data_load("board_pin", name="btn_touch_b",         name_pin="18",  psy_pin=18)
    # umod.data_load("board_pin", name="pin_ledtop_pwm",      name_pin="4",   psy_pin=4)
    # umod.data_load("board_pin", name="pin_ledtable_pwm",    name_pin="5",   psy_pin=5)
    #
    #
    # umod.data_load("board_pin", name="sda_1", name_pin="sda_25", psy_pin=25)
    # umod.data_load("board_pin", name="scl_1", name_pin="scl_26", psy_pin=26)
    #
    # # i2c
    #
    # umod.data_load("cfg_i2c", name="i2c_1", board_pin={"sda": "sda_1", "scl": "scl_1"})
    #
    # # PUSH
    #
    # umod.data_load("cfg_push", name="push_touch",
    #                board_pin="btn_touch",
    #                status=["ON", "OFF"],
    #                pin_mode="IN", pin_pull="PULL_DOWN",
    #                type="click", state=None)
    #
    # umod.data_load("cfg_push", name="push_touch_b",
    #                board_pin="btn_touch_b",
    #                status=["ON", "OFF"],
    #                pin_mode="IN", pin_pull="PULL_DOWN",
    #                type="click", state=None)
    #
    #
    # # RELAY
    #
    # umod.data_load("cfg_relay", name="relay_led",
    #                board_pin="led_status",
    #                value_on=1, value_def=0,
    #                pin_mode="OUT", type="led", state=None)
    #
    # umod.data_load("cfg_relay", name="relay_1",
    #                board_pin="relay_1",
    #                value_on=0, value_def=None,
    #                pin_mode="OUT", type="led", state=None)
    #
    #
    # # PWM
    # umod.data_load("cfg_pwm", name="led_top",
    #               board_pin="pin_ledtop_pwm",
    #               duty=10, freq=200000, timer=0,
    #               value=0,
    #               state=None)
    #
    # umod.data_load("cfg_pwm", name="led_table",
    #               board_pin="pin_ledtable_pwm",
    #               duty=60, freq=200000, timer=0,
    #               value=1,
    #               state=None)
    #
    # umod.data_load("cfg_http", name="default", addr="0.0.0.0", port=8080, path="./www", client=0)
    # umod.data_load("cfg_http_route", name="rpc", route="/rpc", handler="route_rpc")
    # umod.data_load("cfg_http_route", name="dummy", route="/dummy", handler="route_dummy")

