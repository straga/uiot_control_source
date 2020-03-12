

const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useDispatch,  useGetters} = owl.hooks;
import {SelectAction} from "../components/ui/select/Select.js";

export class Device extends Component {


    static components = {SelectAction};

    static template = xml`        
        <div class="bg-light text-dark mt-4">
            <div class="screen">
                <h1 class="text-center "><t t-esc="menuText.name"/></h1>
                <div class="container">
                    
                    <t t-if="state.action === 'devices_connect'">
                        <SelectAction records="hosts_select" action="'host-select-action'"></SelectAction>
                    </t>
                    <t t-if="state.action === 'devices_list'">
<!--                        <ListView records="state.cfg_wifi_ap" model="state.model"></ListView>-->
                    </t>




                </div>
            </div>
        </div>
    `;

    constructor() {

        super(...arguments);
        this.menu = "devices";
        this.hosts_db = "web_ctrl_host";
        this.dispatch = useDispatch();
        this.menus = useStore(state => state.menus);

        this.getters = useGetters();

        this.hosts_select = [];

        this.state = useState({
            action: "devices"
        });

    }

    get menuText() {
        return  this.menus.find(m => m.key === this.menu);
    }

    async willStart() {

        console.log("willstart");
        let self = this;
        let db = this.hosts_db;


        this.env.rpc.request("call", {
          'action': "call_db",
          'param': db,
          'method': "scan",
        }, true
        ).then(function (res) {

            const hosts_select = [];
              res.forEach(function(item){

                   hosts_select.push({
                       title: item.name +" - "+ item.addr,
                       value: item.addr+":"+item.port
                   })

              });

              self.hosts_select = hosts_select;

        });



    }

    mounted() {

        let self = this;
        this.env.bus.on("host-select-action", "devices", function(ev) {
             self.env.rpc.endpoint = "http://"+ev+"/rpc";
             self.env.host = "http://"+ev;
             self.dispatch("addSomeData", {state: "host_name", data: {name: ev }});

             self.env.bus.trigger("host_info");


        });

        this.env.bus.on("menu-func-event", "devices", function(args) {
                self.state.action = args.key;
                self._action()
        });

    }


    willUnmount() {
          this.env.bus.off("host-select-action", "devices");
          this.env.bus.off("menu-func-event", "devices");
    }


    _action() {

        var self = this;
        this.env.bus.trigger("bar-event");

        // if (this.state.action === "scan") {
        //
        //     this.state.model = "wifi";
        //
        //     this.env.rpc.request("call", {
        //         'action': "call_env",
        //         'param': "net",
        //         'method': "wifi.sta.scan_ap",
        //     }).then(function (res) {
        //
        //         console.log(res);
        //         self.dispatch("addSomeData", {state: "scanAP", data: res});
        //         // self.dispatch("addSomeData", {state: "Records", data: res});
        //
        //     });
        // }

    }




  }