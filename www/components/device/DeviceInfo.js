const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useDispatch} = owl.hooks;

export class DeviceInfo extends Component {

    static template = xml`  
        <div>
            Device: <t t-esc="device_info.release"/>, <t t-esc="device_info.machine"/>,  <t t-esc="device_info.partition"/>
        </div>          
    `;

    constructor() {
          super(...arguments);

          this.dispatch = useDispatch();
          this.dispatch("addSomeData", {state: "device_info", data:[]});
          this.device_info = useStore((state) => state.device_info);



    }
    mounted() {

        let self = this;
        this.env.bus.on("device_info", "devices", function() {
                self._action()
        });

    }

    _action() {

        this.dispatch("addSomeData", {state: "device_info", data:[] });

        let self = this;
        this.env.rpc.request("call", {
          'action': "call_env",
          'param': "board",
          'method': "uname",
        }, false
        ).then(function (res) {

            let info ={
                "sysname": res[0],
                "nodename": res[1],
                "release": res[2],
                "version": res[3],
                "machine": res[4]
            }
            self.dispatch("addSomeData", {state: "device_info", data:info });
        });

    }

}
