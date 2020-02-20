
import logging
log = logging.getLogger('TEST')
logging.basicConfig(level=logging.DEBUG)



def config_simple(g_config, json_data="."):


    log.info("{}".format("Conf MOD - START"))

    log.info("Normal JSON")
    g_config.from_file("{}/board.json".format(json_data))

    log.info("Empty JSON")
    g_config.from_file("{}/board_empty.json".format(json_data))

    log.info("Error JSON")
    g_config.from_file("{}/board_empty_error.json".format(json_data))

    log.info("Empty File")
    g_config.from_file("{}/board_empty_none.json".format(json_data))

    log.info("board_cfg")
    g_config.from_file("{}/board_cfg.json".format(json_data))

    log.info("board_mod")
    g_config.from_file("{}/board_mod.json".format(json_data))


    json_string_schema = """
    {
        "_schema-1": {
            "_schema" : "_schema",
            "name": "string_mod",
            "sch": [
                      ["name",  ["str", ""      ]],
                      ["type",  ["str", "No"    ]],
                      ["active",["bool", true   ]],
                      ["seq",   ["int", 10]     ]
            ],
            "_upd": true
        }
    }
    """


    json_string_data = """
    {
        "01": {
            "_schema" : "string_mod",
            "name": "str_1",
            "seq": 1
        },

        "02": {
            "name": "str_2"
        },

        "03": {
            "_schema" : "string_mod",
            "name": "str_3",
            "seq": 5
        },
        
        "04": {
            "_schema" : "string_mod",
            "name": "str_4",
            "seq": 15,
            "_upd": true
        }

    }
    """

    log.info("String SCH")
    g_config.from_string(json_string_schema)

    log.info("String DATA")
    g_config.from_string(json_string_data)

    log.info("Select One")
    g_config.select_one("string_mod", "str_1")

    log.info("Scan Name")
    for _scan_name in g_config.scan_name("string_mod"):
        log.info("SCAN NAME: {}".format(_scan_name))

        obj_sel = g_config.select_one("string_mod", _scan_name)
        log.info("DATA: {}".format(obj_sel))

    log.info("Select One Object")
    obj_1 = g_config.select_one("string_mod", "str_4", True)

    log.info(obj_1._schema)
    log.info(obj_1.name)
    log.info(obj_1.seq)
    log.info(obj_1.type)
    log.info(obj_1.active)

    log.info("__dict__: {}".format(obj_1.__dict__))

async def config_async(g_config):


    log.info("SELECT/UPDATE OBJECT")

    obj_1 = await g_config.call("select_one", "string_mod", "str_4", True)

    if obj_1:

        if obj_1.type == "updated":
            obj_1.type = "Not updated"
        else:
            obj_1.type = "updated"

        await obj_1.update()

    obj_up4 = await g_config.call("select_one", "string_mod", "str_4", True)

    if obj_up4:
        log.info("__dict__: {}".format(obj_up4.__dict__))



    log.info("SAVE DATA - not OBJECT - ONE element in dict")

    dic_upd = {'type': 'ONE_updated'}

    await g_config.call("from_dict", "string_mod", "str_4", dic_upd)

    obj_up_one = await g_config.call("select_one", "string_mod", "str_4", False)

    if obj_up_one:
        log.info(obj_up_one)


    _modules = await g_config.call("scan", "string_mod")
    log.info("Random".format(_modules))
    _modules = sorted(_modules, key=lambda i: i['seq'])
    log.info("Sorted".format(_modules))



