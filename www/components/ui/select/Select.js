

const { xml, css} = owl.tags;
const { Component, useState } = owl;

const TEMPLATE = xml/* xml */ `
        
            <select t-on-change="setOnchange" class="form-control">
                
               
                <option t-if="!state.select" value="">Please select</option>
                
                <option t-foreach="props.records" t-as="record" t-key="record_index" t-att-value="record.value">
                    <t t-esc="record.title"/>
                </option>
            </select>
 
        `;


const STYLE = css/* css */ `
  // .main {
  //   display: grid;
  //   grid-template-columns: 200px auto;
  // }
`;


export class SelectAction extends Component {

        static template = TEMPLATE;
        static style = STYLE;

        constructor() {
            super(...arguments);
            var self = this;

            this.state = useState({ select: false,
            });
        }

        static defaultProps = {
                records: {},
                action: false
        };


        setOnchange(ev) {
            // console.log(ev.target.value)
            if (this.props.action){
                this.env.bus.trigger(this.props.action, ev.target.value);
            }
            this.state.select = true;

        }



  }