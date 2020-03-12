
const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useRef, useDispatch } = owl.hooks;


import { ListView } from "../components/ui/listview/ListView.js";


export class Hardware extends Component {


        static components = {ListView};
        static template = xml`        
        <div class="bg-light text-dark mt-4">
            <div class="screen">
                <h1 class="text-center ">
                    <t t-esc="menuText.name"/>
                </h1>
                <div class="container">
                
                    <t t-if="state.action === 'hw_pin_value'">
                        <ListView model="state.model" add="false" edit="false"></ListView>
                    </t>      
                    
                    
                </div>
            </div>
        </div>
        `;

      constructor() {

            super(...arguments);
            var self = this;
            this.menu = "hw";

            this.menus = useStore(state => state.menus);
            this.dispatch = useDispatch();

            this.state = useState({
                action: false,
                active_menu: "home",
                model: false,
            });

      }

      async willStart() {
            console.log("willstart");
      }

      mounted() {
          var self = this;

          this.env.bus.on("menu-func-event", "hw", function(args) {
                self.state.action = args.key;
                self._action()
          });

          this.env.bus.on("store-update", "hw", function(ev) {
                self._action()
          });

          // console.log("mounted");

          setInterval(() => self.pin_val_update(), 5000);

      }

      willUnmount() {
          this.env.bus.off("menu-func-event", "hw");
          this.env.bus.off("store-update", "hw");

      }

      pin_val_update(){

          var self = this;

          if (this.state.action === "hw_pin_value") {

              this.state.model = "hw_control_pin";

              this.env.rpc.request("call", {
                  'action': "call_env",
                  'param': "hw_control",
                  'method': "pin_value",
                  'args': ["pin_cfg"]
              }).then(function (res) {

                  console.log(res);
                  // self.dispatch("addSomeData", {state: "scanAP", data: res});
                  self.dispatch("updateTargetData", {state: "record_db", target: "hw_control_pin", data: res});

                  // self.dispatch("addSomeData", {state: "Records", data: res});

              });
          }


      }



    _action(){

        this.pin_val_update()



          this.env.bus.trigger("bar-event");

      }

      get menuText() {

          return  this.menus.find(m => m.key === this.menu);
      }


  }
