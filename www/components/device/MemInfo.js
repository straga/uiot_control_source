const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useDispatch} = owl.hooks;

export class MemInfo extends Component {

        static template = xml`  
        <div>
            Mem - Free: <t t-esc="mem_info.free"/>, Alloc: <t t-esc="mem_info.alloc"/>
        </div>
              
           
    `;

    constructor() {
          super(...arguments);

          this.dispatch = useDispatch();
          this.dispatch("addSomeData", {state: "mem_info", data:[]});
          this.mem_info = useStore((state) => state.mem_info);


    }
    mounted() {
        let self = this;



        this.env.bus.on("mem_info", "devices", function() {
            self._action()
        });

        setInterval(() => self.env.bus.trigger("mem_info"), 10000);

    }

    unmount() {
        super.unmount();
    }


    _action() {


        let self = this;
        this.env.rpc.request("call", {
          'action': "call_env",
          'param': "board",
          'method': "mem_info",
        }, false
        ).then(function (res) {

            let info ={
                "free": res[0],
                "alloc": res[1],
            }
            self.dispatch("addSomeData", {state: "mem_info", data:info });
        }).catch(
            self.dispatch("addSomeData", {state: "mem_info", data:[] })

        );

    }





}
