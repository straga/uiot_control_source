const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useDispatch} = owl.hooks;

export class PartitionInfo extends Component {

    static template = xml`  
        <div>
            Partition Current: <t t-esc="part_info.current"/>
        </div>          
    `;

    constructor() {
          super(...arguments);

          this.dispatch = useDispatch();
          this.dispatch("addSomeData", {state: "part_info", data:[]});
          this.part_info = useStore((state) => state.part_info);



    }
    mounted() {

        let self = this;
        this.env.bus.on("device_info", "partition", function() {
            self._action()
        });

    }

    _action() {

        this.dispatch("addSomeData", {state: "part_info", data:[] });
        let self = this;
        this.env.rpc.request("call", {
          'action': "call_env",
          'param': "board",
          'method': "get_part",
        }, false
        ).then(function (res) {
            let info ={
                "current": res,
            }
            self.dispatch("addSomeData", {state: "part_info", data:info });
        });


    }

}
