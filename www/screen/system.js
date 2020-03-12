

const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useRef, useDispatch } = owl.hooks;
import { ListView } from "../components/ui/listview/ListView.js";
import { SelectAction } from "../components/ui/select/Select.js";



export class System extends Component {


    static components = {ListView, SelectAction};

    static template = xml`        
        <div class="bg-light text-dark mt-4">
            <div class="screen">
                <h1 class="text-center "><t t-esc="menuText.name"/></h1>
                <div class="container">
                        <t t-if="state.action === 'tables'">
                            <SelectAction records="scan_db" action="'system-select-action'"></SelectAction>
                        </t>
                        
                        <t t-if="state.list_db and state.action === 'tables'">
                            <ListView model="state.list_db"></ListView>
                        </t>
                        
                        <t t-if="state.action === 'restart'">
                            <SelectAction records="boot_select" action="'restart-board'"></SelectAction>
                        </t>
                        
                        <t t-if="state.action === 'wait'">
                            Wait
                        </t>
                        
                </div>
            </div>
        </div>
    `;

    constructor() {

        super(...arguments);
        this.menu = "system";
        this.menus = useStore(state => state.menus);
        this.dispatch = useDispatch();
        // this.dispatch("addSomeData", {state: "scan_db", data:[]});
        this.dispatch("addSomeData", {state: "record_db", data:[]});
        // this.dispatch("addSomeData", {state: "_schema", data:[]});

        this.scan_db = useStore(state => state.scan_db);

        this.boot_select = [
            {title: "Restart", value: "restart" },
            {title: "Boot in ota_0", value: "ota_0" },
            {title: "Boot in factory", value: "factory" }
        ]



        this.record_db = useStore(state => state.record_db);
        this._schema = useStore(state => state._schema);
        this.state = useState({ action: false,
                model: false,
                list_db: false,
            });

    }

    mounted() {
          var self = this;

          this.env.bus.on("menu-func-event", "system", function(args) {
                self.state.action = args.key;
                self.scan_action()
          });

          this.env.bus.on("system-select-action", "system", function(ev) {
              self.list_action(ev)
          });

          this.env.bus.on("store-update", "system", function(ev) {
                self.list_action()
          });

          this.env.bus.on("restart-board", "system", function(ev) {
              self.restart_action(ev)
          });

    }


    willUnmount() {
          this.env.bus.off("menu-func-event", "system");
          this.env.bus.off("system-select-action", "system");
          this.env.bus.off("store-update", "system");
          this.env.bus.off("restart-board", "system");
    }


    restart_action(ev=false){
        let self = this;
        let part_for_boot = ev;
        let params = {}

        if (["ota_0", 'factory'].includes(part_for_boot)){
            params['args'] = [part_for_boot]
        }

        this.env.rpc.request("call", {
                  'action': "call_env",
                  'param': "board",
                  'method': "reboot",
                  ... params
              });

        self.state.action = "wait"

     }


     list_action(ev=false){
        let self = this;
        let db = this.state.list_db;
        if (ev){
            db = ev
            self.state.list_db = false;
        }

        if (db){
            this.env.rpc.request("call", {
                  'action': "call_db",
                  'param': db,
                  'method': "scan",
              }).then(function (res) {
                  self.dispatch("updateTargetData", {state: "record_db", target: db, data: res});
                  self.state.list_db = db;
              });
        }
     }

    scan_action(){

          var self = this;

          this.env.bus.trigger("bar-event");

      }


    get menuText() {
        return  this.menus.find(m => m.key === this.menu);
    }

  }
