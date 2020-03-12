const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useDispatch} = owl.hooks;

export class BoardInfo extends Component {

    static template = xml`  
        <div>
            Board: <t t-esc="board_info.hostname"/> - <t t-esc="board_info.uid"/>
        </div>          
    `;

    constructor() {
          super(...arguments);

          this.dispatch = useDispatch();
          this.dispatch("addSomeData", {state: "board_info", data:[]});
          this.board_info = useStore((state) => state.board_info);



    }
    mounted() {

        let self = this;
        this.env.bus.on("device_info", "devices", function() {
                self._action()
        });

    }

    _action() {

        this.dispatch("addSomeData", {state: "board_info", data:[] });

        let self = this;
        this.env.rpc.request("call", {
          'action': "call_env",
          'param': "board",
          'method': "board.uid"
        }, false
        ).then(function (res) {

            self.dispatch("updateTargetData", {state: "board_info", target:"uid", data:res });
        });

        this.env.rpc.request("call", {
          'action': "call_env",
          'param': "board",
          'method': "board.hostname"
        }, false
        ).then(function (res) {

            self.dispatch("updateTargetData", {state: "board_info", target:"hostname", data:res });
        });




    }

}
