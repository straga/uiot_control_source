import { initialState, screensList }  from "./init.js";

function app() {


  const { Component, useState } = owl;
  const { useStore, useRef } = owl.hooks;
  const bus = new owl.core.EventBus();

  const LOCALSTORAGE_KEY = "upy";

  const actions = {};

  class MobileMenu extends Component {

      toggle() {
          this.trigger("collapse-menu", { state: this.props.state });
      }
  }


  class Navbar extends Component {
      constructor() {
          super(...arguments);
          this.menus = useStore(state => state.menus);
      }

      state = useState({ collapse: true, filter: "all", active_menu: "home" });

      get visibleMenu() {
          var self = this;
          switch (this.state.filter) {
                case "all": return self.menus;
          }
      }

      collapseMenu(ev) {
          this.state.collapse = !this.state.collapse;
      }

      toggleMenu(ev) {
          this.state.active_menu = ev;
          bus.trigger("menu-event", ev);
      }

  }




  Navbar.components = { MobileMenu };


  class ControlPanel extends Component {}

  class Footer extends Component {}



  class Screen extends Component {

    // get style() {
    //   let { width, height, top, left, zindex } = this.props.info;
    //   return `width: ${width}px;height: ${height}px;top:${top}px;left:${left}px;z-index:${zindex}`;
    // }
    //
    // close() {
    //   this.trigger("close-window", { id: this.props.info.id });
    // }

  }

  class ScreenManager extends Component {
    constructor() {
      super(...arguments);
      this.screensList = false;
      this.nextId = 1;
    }

    addScreen(name) {
      const info = this.env.screensList.find(w => w.name === name);
      if (info){
          this.screen = {
            id: this.nextId++,
            title: info.title,
            component: info.component
          }

      }else{
        this.closeScreen()
        }


      this.render();
    }

    closeScreen() {
      // const id = ev.detail.id;
      delete this.constructor.components[this.nextId];
      this.screen = false;
      this.render();
    }

  }
  ScreenManager.components = { Screen };



  class App extends Component {

    constructor() {
        super(...arguments);
        var self = this;
        this.wmRef = useRef("wm");
        this.menus = useStore(state => state.menus);

        bus.on("menu-event", null, function(args) {
                        self.state.active_screen = args;
                        self.addScreen(args)

        });


    }

    mounted() {
        this.addScreen(this.state.active_screen);
    }


    addScreen(name) {
      this.wmRef.comp.addScreen(name);
    }

    state = useState({ active_screen: "home"});

  }

  App.components = { Navbar, ControlPanel, Screen, ScreenManager, Footer };
  App.env.screensList = screensList;





  function makeStore() {
      function saveState(state) {
          const str = JSON.stringify(state);
          window.localStorage.setItem(LOCALSTORAGE_KEY, str);
      }
      function loadState() {
          const localState = window.localStorage.getItem(LOCALSTORAGE_KEY);
          return localState ? JSON.parse(localState) : initialState;
      }

      const state = loadState();
      const store = new owl.Store({ state, actions });
      store.on("update", null, () => saveState(store.state));
      return store;
  }

  //------------------------------------------------------------------------------
  // Responsive plugin
  //------------------------------------------------------------------------------
  function setupResponsivePlugin(env) {
      const isMobile = () => window.innerWidth <= 768;
      env.isMobile = isMobile();
      const updateEnv = owl.utils.debounce(() => {
          if (env.isMobile !== isMobile()) {
              env.isMobile = !env.isMobile;
              env.qweb.forceUpdate();
          }
      }, 15);
      window.addEventListener("resize", updateEnv);
  }



    // debugOwl(owl, {
    //   // componentBlackList: /App/,  // regexp
    //   // componentWhiteList: /SomeComponent/, // regexp
    //   // methodBlackList: ["mounted"], // list of method names
    //   // methodWhiteList: ["willStart"], // list of method names
    //   logScheduler: true, // display/mute scheduler logs
    //   logStore: true // display/mute store logs
    // });

  //------------------------------------------------------------------------------
  // Application Startup
  //------------------------------------------------------------------------------
  setupResponsivePlugin(App.env);
  App.env.store = makeStore();

  const app = new App();
  app.mount(document.body);



}

/**
 * Initialization code
 * This code load templates, and make sure everything is properly connected.
 */
async function start() {
    owl.config.mode = "dev";
    let templates;
    try {
    templates = await owl.utils.loadFile('app.xml');
    // await owl.utils.loadJS('./screen/home.js');
    // await owl.utils.loadJS('./screen/wifi.js');



    } catch(e) {
    console.error(`This app requires a static server`);
    return;
    }
    const env = { qweb: new owl.QWeb({templates})};
    // env.qweb.dev = "dev";
    owl.Component.env = env;
    await owl.utils.whenReady();
    app();
}


start();
