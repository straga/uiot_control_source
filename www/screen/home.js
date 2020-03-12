

const { Component, useState } = owl;
const { useStore, useRef } = owl.hooks;

export class Home extends Component {

      constructor() {

        super(...arguments);
        this.menu = "home";
        this.menus = useStore(state => state.menus);

      }

      get menuText() {

          return  this.menus.find(m => m.key === this.menu);
      }

  }
