
const { xml, css} = owl.tags;
const { Component, useState } = owl;
const { useStore, useRef, useDispatch, useGetters } = owl.hooks;

const TEMPLATE = xml/* xml */`
        <table class="table table-striped">
        
            <thead class="data_head">
<!--               <t t-set="HEAD" t-value="getData('head')"/>-->
               <tr>
                    <th t-foreach="storeSch" t-as="record" >
                        <t t-esc="record"/>
                    </th>
                    
                    
                    <th t-if="props.action">
                        Action
                    </th> 
                    <th t-if="!state.new and props.model and props.add">
                        <div class="btn-group btn-group-sm">
                            <button type="button" class="btn btn-outline-success" 
                                    t-on-click.stop="addClick()">Add</button>
                        </div>
                    </th>  
               </tr>
            </thead>
            
            <tbody class="data_body">
                <tr t-foreach="storeRecords" t-as="records" t-on-click="editClick(records)">
<!--                <t t-log="records"/>-->
                        
                        
                     <t t-set="is_edit" t-value="isEdit(records)"/>
                     
                     <td t-foreach="storeSch" t-as="head_key">
 
                        <t t-if="!isFkey(head_key, is_edit)">
                      
                             <t t-esc="records[head_key]" />
                        
                        </t>
                        <t t-if="isFkey(head_key, is_edit)">
                            <input class="tabledit-input form-control input-sm" 
                            type="text" 
                            t-att-value="records[head_key]"
                            t-att-id="head_key"
                            t-att-name="records[props.fkey]" 
                            t-on-input="_updateInputValue"/>
                        </t>

                    </td>
                    
                    
                    <td t-if="props.action">
<!--                    <t t-log="props.action" />-->
                        <div class="btn-group btn-group-sm">
                            <button t-foreach="props.action" 
                                    t-as="act" type="button" class="btn btn-outline-success" 
                                    t-on-click.stop="actionClick(records, act.act)">
                                 <t t-esc="act.name" />
                            </button>
                        </div>
                    </td> 
                    
                    
                    <td t-if="is_edit">
                        
                            <div class="btn-group btn-group-sm">
                                <button type="button" class="btn btn-outline-success" t-on-click.stop="saveClick(records)">Save</button>
                                <button type="button" class="btn btn-outline-secondary" t-on-click.stop="saveClick">Cancel</button>
                                <button type="button" class="btn btn-outline-danger" t-on-click.stop="delClick">Del</button>
                            </div>
                         
                    </td>
                    
                </tr>
            </tbody>
        </table>
        `;


const STYLE = css/* css */ `
  // .main {
  //   display: grid;
  //   grid-template-columns: 200px auto;
  // }
`;


export class ListView extends Component {

        static template = TEMPLATE;
        static style = STYLE;


        constructor() {
            super(...arguments);
            var self = this;
            this._update = {};
            this.dispatch = useDispatch();
            this.getters = useGetters();
            this.records = useStore(state => state.scan_db);

        }

        async willStart() {

            this.schema = useStore(state => state._schema)
        }

        static defaultProps = {
                fkey: 'name',
                add: true,
                del: true,
                edit: true,
                save: true,
                model: false,
                action: false,
                record_db: "record_db",
                schema: "_schema"
        };

        getters = useGetters();

        storeSch = useStore((state, props) => {

            let _sch_list = this.getters.getSomeData({state: props.schema, data:props.model});

            if (_sch_list){
                let _sch = _sch_list.find(s => s.name === this.props.model)
                if (_sch){
                    return _sch.sch
                }

            }
            return []

            // return state._schema.find(s => s.name === this.props.model).sch

        });

        storeRecords = useStore((state, props) => {
              let _records =  this.getters.getSomeData({state: props.record_db, data: props.model});

              if (_records) {
                  return _records
              }

              return []

        });

        state = useState({
            rowEditing: false,
            new: false,
            modelEdit: false
        });


        editClick(ev) {

            if (this.props.edit) {

                if (this.props.model !== this.state.modelEdit) {
                    this.state.modelEdit = this.props.model;
                    this.state.rowEditing = false
                }

                if (this.props.model && !this.state.rowEditing) {
                    this.state.rowEditing = ev[this.props.fkey];
                }

            }

        }

        isFkey(ev, ed){

            if (ed && this.props.fkey === ev){
                return !!this.state.new;

            }else if(ed && this.props.fkey !== ev) {
                return true;
            }
            return false
        }


        isEdit(ev){

            if (this.props.model && this.props.edit){

               return ev[this.props.fkey] === this.state.rowEditing;
            }else{
                return false
            }
        }


        _updateInputValue(ev){
            this._update[ev.target.id] = ev.target.value
        }

        saveClick(ev){
            console.log("SAVE");
            console.log(ev);
            let self = this;

            if (ev && Object.entries(this._update).length !== 0){

                let params = {}
                let _name = this.state.rowEditing

                if (this.state.new){
                     _name = this._update[this.props.fkey]
                }

                params['args'] = [_name , this._update]

                this.env.rpc.request("call", {
                  'action': "call_db",
                  'param': this.props.model,
                  'method': "from_dict",
                    ...params

                    }).then(function (res) {
                        self.env.bus.trigger("store-update");
                    });
            }else{
                self.env.bus.trigger("store-update");
            }

            this.state.rowEditing = false;
            this._update = {};
            this.state.new = false;

        }


        delClick(ev){
            console.log("DEL");
            console.log(ev);

            let self = this;

            if (!this.state.new) {
                this.env.rpc.request("call", {
                    'action': "call_db",
                    'param': this.props.model,
                    'method': "delete",
                    'args': [{[this.props.fkey]: this.state.rowEditing}],

                }).then(function (res) {
                    self.env.bus.trigger("store-update");
                });
            }
            else{
                self.env.bus.trigger("store-update");
            }

            this.state.rowEditing = false;
            this._update = {};

        }

        addClick(ev) {

            console.log("ADD");
            console.log(ev);
            let self = this;
            let data = {};

            for(let key in this.storeSch){

                if (self.props.fkey === key){
                    data[key] = "New"
                }
                else{
                    if (Object.entries(this.storeSch[key]).length > 0){

                        data[key] = this.storeSch[key][1]
                    }
                    else{

                        data[key] = this.storeSch[key]
                    }


                }
            }


            if (Object.entries(data).length > 0){

                this.state.new = true;
                this.state.rowEditing = "New";
                this._update = {};
                this.dispatch("pushTargetData", {state: this.props.record_db, target:this.props.model, data:data});
            }
        }


        actionClick(rec, trigger){

           // console.log("ACTION: "+ev);
           this.env.bus.trigger(trigger, rec);

        }

  }