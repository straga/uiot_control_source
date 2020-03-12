

const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useRef, useDispatch } = owl.hooks;
// import { Footer } from "./Footer.js";


import { ListView } from "../components/ui/listview/ListView.js";




export class WiFi extends Component {


        static components = {ListView};
        static template = xml`        
        <div class="bg-light text-dark mt-4">
            <div class="screen">
                <h1 class="text-center ">
                    <t t-esc="menuText.name"/>
                </h1>
                <div class="container">
                    <t t-if="state.action === 'scan'">
                        <ListView model="state.model" action="actions"></ListView>
                    </t>
                    <t t-if="state.action === 'ap'">
                        <ListView model="state.model"></ListView>
                    </t>
                    <t t-if="state.action === 'station'">
                        <ListView model="state.model"></ListView>
                    </t>
                                    
<!--                     <ListView records="state.Records" fkey="'name'" model="state.model"></ListView>-->
                 
                    
                </div>
            </div>
        </div>
        `;

      constructor() {

            super(...arguments);
            var self = this;
            this.menu = "wifi";

            this.actions = [
                {name:"ADD", act: "push-to-station"}
            ]

            this.menus = useStore(state => state.menus);
            this.dispatch = useDispatch();

            // this.dispatch("addSomeData", {state: "scanAP", data:[]});

            // this.dispatch("addSomeData", {state: "wifi_ap_cfg", data:[]});
            // this.dispatch("addSomeData", {state: "wifi_sta_cfg", data:[]});
            // this.dispatch("addSomeData", {state: "Records", data:[]});

            this.state = useState({ action: false, filter: "all", active_menu: "home",
                model: false,
                // scanAP: useStore(state => state.scanAP),
                // wifi_ap_cfg: useStore(state => state.wifi_ap_cfg),
                // wifi_sta_cfg: useStore(state => state.wifi_sta_cfg),
                // Records:useStore(state => state.Records),
            });

      }

      async willStart() {
            console.log("willstart");
      }

      mounted() {
          var self = this;

          this.env.bus.on("menu-func-event", "wifi", function(args) {
                self.state.action = args.key;
                self._action()
          });

          this.env.bus.on("store-update", "wifi", function(ev) {
                self._action()
          });

          this.env.bus.on("push-to-station", "wifi", function(ev) {

              console.log("push-to-station: "+ev);
                self.add_station(ev)

          });

          // console.log("mounted");

      }

      willUnmount() {
          this.env.bus.off("menu-func-event", "wifi");
          this.env.bus.off("store-update", "wifi");
          this.env.bus.off("push-to-station", "wifi");

          // console.log("willUnmount");
      }


      // state = useState({ collapse: true, filter: "all", active_menu: "home" });



    add_station(ev){
            const self = this;
          let add_sta = {
              name: ev["ssid"],
              ssid: ev["ssid"],
          };

          this.env.rpc.request("call", {
                  'action': "call_db",
                  'param': "wifi_sta_cfg",
                  'method': "from_dict",
                  'args' : [ ev["ssid"] , add_sta]

                    }).then(function (res) {
                        self.state.action = "station";
                        self.env.bus.trigger("store-update");

                    });

    }

    _action(){

          var self = this;


          if (this.state.action === "scan") {

              this.state.model = "wifi_scan_map";

              this.env.rpc.request("call", {
                  'action': "call_env",
                  'param': "net",
                  'method': "wifi.sta.scan_ap",
              }).then(function (res) {

                  console.log(res);
                  // self.dispatch("addSomeData", {state: "scanAP", data: res});
                  self.dispatch("updateTargetData", {state: "record_db", target: "wifi_scan_map", data: res});

                  // self.dispatch("addSomeData", {state: "Records", data: res});

              });
          }



          if (this.state.action === "ap") {
              console.log("AP");

              this.state.model = "wifi_ap_cfg";

              this.env.rpc.request("call", {
                  'action': "call_db",
                  'param': "wifi_ap_cfg",
                  'method': "scan",
              }).then(function (res) {

                  console.log(res);
                  self.dispatch("updateTargetData", {state: "record_db", target: "wifi_ap_cfg", data: res});
              });
          }


          if (this.state.action === "station") {
              this.state.model = "wifi_sta_cfg";


              this.env.rpc.request("call", {
                  'action': "call_db",
                  'param': "wifi_sta_cfg",
                  'method': "scan",
              }).then(function (res) {

                  console.log(res);
                  self.dispatch("updateTargetData", {state: "record_db", target: "wifi_sta_cfg", data: res});

              });
          }


          this.env.bus.trigger("bar-event");

      }

      get menuText() {

          return  this.menus.find(m => m.key === this.menu);
      }


  }
