import { MobileMenu } from "./MobileMenu.js";

const { Component, useState } = owl;
const { useStore} = owl.hooks;

export class Navbar extends Component {

    static components = { MobileMenu };

  constructor() {
      super(...arguments);
      this.menus = useStore(state => state.menus);
  }

  state = useState({ collapse: true, filter: "all", active_menu: "home" });


  get visibleMenu() {
      var self = this;
      switch (this.state.filter) {
            // case "all": return self.menus.find(m => m.parent === "");
            case "all": return self.menus.filter(m => !m.parent);
      }
  }

  subMenu(parent) {

      if (this.state.active_menu === this.props.active_screen) {
          return this.menus.filter(m => m.parent === parent);
      }
      return []
  }

  collapseMenu(ev) {
      this.state.collapse = !this.state.collapse;
  }

  collapseBar(){
      this.env.bus.trigger("bar-event");
  }


  toggleMenu(ev) {

      if (ev.action === "screen"){
          this.state.active_menu = ev.key;
          this.env.bus.trigger("menu-event", ev.key);
      }
      else if(ev.action === "func"){
          this.env.bus.trigger("menu-func-event", ev);
      }
  }

}
