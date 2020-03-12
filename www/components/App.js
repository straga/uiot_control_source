import { StatusTop } from "./StatusTop.js";
import { Footer } from "./Footer.js";
import { Navbar } from "./Navbar.js";
import { ScreenManager } from "./ScreenManager.js";

const { Component, useState } = owl;
const { useStore, useRef } = owl.hooks;

export   class App extends Component {

    constructor() {
        super(...arguments);
        var self = this;
        this.wmRef = useRef("wm");
        this.menus = useStore(state => state.menus);

        this.env.bus.on("menu-event", null, function(args) {
                        self.state.active_screen = args;
                        self.addScreen(args)

        });

        this.env.bus.on("bar-event", null, function(args) {
            self.state.active_bar = false;

        });

    }

    mounted() {
        this.addScreen(this.state.active_screen);
    }


    addScreen(name) {
      this.wmRef.comp.addScreen(name);
    }

    state = useState({ active_screen: "home", active_bar: false});


    toggleBar() {
      this.state.active_bar = !this.state.active_bar;
      // this.env.bus.trigger("menu-event", ev);
    }

  }

  App.components = {StatusTop, Navbar, ScreenManager, Footer };
  // App.components = { Navbar, ControlPanel, ScreenView, ScreenManager, Footer };
