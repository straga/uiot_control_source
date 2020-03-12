const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useDispatch} = owl.hooks;

export class HostInfo extends Component {

    static template = xml`  
        <div>
            Host: <t t-esc="host_name.name"/> 
        </div>          
    `;

    constructor() {
          super(...arguments);

          this.dispatch = useDispatch();
          this.dispatch("addSomeData", {state: "host_name", data:{name:"No set"} });
          this.host_name = useStore((state) => state.host_name);
    }

    mounted() {

        let self = this;
        this.env.bus.on("host_info", "devices", function() {
            self._action()
        });

    }

    _action() {

        this.dispatch("addSomeData", {state: "scan_db", data: []});
        this.dispatch("addSomeData", {state: "_schema", data: []});
        this.dispatch("addSomeData", {state: "record_db", data:[]});

        let self = this;

        this.env.rpc.request("call", {
          'action': "call_db",
          'param': "_schema",
          'method': "scan",
        }).then(function (res) {

          // console.log(res);
          const copy = [];


            res.forEach(function(item){
                 copy.push({
                     title: item.name,
                     value: item.name
                 })
            });

            // console.log(copy);

            self.dispatch("addSomeData", {state: "scan_db", data: copy});
            self.dispatch("addSomeData", {state: "_schema", data: res});
            // this.env.bus.trigger("device_info");
            self.env.bus.trigger("device_info");
        });
    }
    
}
