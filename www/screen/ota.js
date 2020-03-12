// cfg_ota_server

const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useRef, useDispatch } = owl.hooks;
import { ListView } from "../components/ui/listview/ListView.js";





export class OTA extends Component {


    static components = {ListView};

    static template = xml`        
        <div class="bg-light text-dark mt-4">
            <div class="screen">
                <h1 class="text-center "><t t-esc="menuText.name"/></h1>
                <div class="container">
                
                 
                    <div>
                    </div>
                    
                    <t t-if="state.action === 'ota_manual'">
                    <h2 class="text-center ">Manual Update: VFS/Flash</h2>
                         <input type="file" name="file-input" t-model="state.file" t-ref="file"/>
                         <button t-on-click.stop="actionClick">Upgrade</button>
                         
                         <progress min="0" max="100" t-att-value="state.progress"></progress>
                    </t>
                     
                          
                     <t t-if="state.action === 'ota_server'">
                        <ListView records="state.cfg_ota_server" model="state.model"></ListView>
                    </t>
                    

                    
           
                </div>
            </div>
        </div>
    `;

    constructor() {

        super(...arguments);
        this.menu = "ota";
        this.wmRef = useRef("file");
        this.menus = useStore(state => state.menus);
        this.dispatch = useDispatch();
        this.dispatch("addSomeData", {state: "cfg_ota_server", data:[]});
        this.state = useState({ action: false,
                model: false,
                cfg_ota_server : useStore(state => state.cfg_ota_server),
                progress: 0,
                part_name: false
            });

    }

    mounted() {
          var self = this;

          this.env.bus.on("menu-func-event", "ota", function(args) {
                self.state.action = args.key;
                self._action()
          });
          this.env.bus.on("store-update", "ota", function(ev) {
                self._action()
          });

    }

    willUnmount() {
          this.env.bus.off("menu-func-event", "ota");
          this.env.bus.off("store-update", "ota");
    }






    _action(){

          var self = this;

          // if (this.state.action === "ota_server") {
          //     this.state.model = "cfg_ota_server";
          //
          //     this.env.rpc.request("call", {
          //         'action': "call_db",
          //         'param': "cfg_ota_server",
          //         'method': "_scan_head",
          //     }).then(function (res) {
          //
          //         console.log(res);
          //         self.dispatch("addSomeData", {state: "cfg_ota_server", data: res});
          //
          //     });
          // }

        // this.env.rpc.request("call", {
        //   'action': "call_env",
        //   'param': "ota_upd",
        //   'method': "partition.get_part",
        // }, false
        // ).then(function (res) {
        //     self.state.part_name = res
        // });

        this.env.bus.trigger("bar-event");

      }


    getHash(buffer, algo = "SHA-256") {
        return crypto.subtle.digest(algo, buffer)
            .then(hash => {
              // here hash is an arrayBuffer, so we'll convert it to its hex version
              let result = '';
              const view = new DataView(hash);
              for (let i = 0; i < hash.byteLength; i += 4) {
                result += ('00000000' + view.getUint32(i).toString(16)).slice(-8);
              }
              return result;
            });
    }

    _update_status(){
        let self = this;
        let err_n = 0
        let myInterval = setInterval(function () {

        self.env.rpc.request("call", {
          'action': "call_env",
          'param': "ota_upd",
          'method': "status"
        }, false
        ).then(function (res) {
           self.state.progress = parseFloat(res)*100
            err_n = 0
        }).catch(function(error) {
            err_n = err_n +1;
            if (err_n > 5){
                clearInterval(myInterval)
            }

        })

        }, 10000);





    }


	actionClick(ev) {
        var self = this;
        self.state.progress = 0

        console.log("ACTION: " + ev);
        let file = this.wmRef.el.files[0];

        const fR = new FileReader();

        let rqq = self.env.host+"/flash";
        self._update_status()

        fR.onload = e => this.getHash(fR.result)
            .then(
                hash => {
                    console.log(hash)
                    fetch(rqq, {

                      method: 'POST',
                      headers: {
                            "SHA256": hash
                        },
                        body: file
                      }).then(response => {
                        return response.blob();
                      });

                }
            )
            .catch(e => {
                console.log(e.message)
            });

        fR.readAsArrayBuffer(file);
      }

      get menuText() {
        return  this.menus.find(m => m.key === this.menu);
    }

  }