import { ScreenView } from "./ScreenView.js";

const { Component} = owl;

 export class ScreenManager extends Component {

     static components = { ScreenView};
     constructor() {
      super(...arguments);
      this.screenList = false;
      this.nextId = 1;
    }

    addScreen(name) {
      const info = this.env.store.state.screensList.find(w => w.name === name);
      if (info){
          this.screenList = {
            id: this.nextId++,
            title: info.title,
            component: info.component
          }

      }else{
          this.screenList = false;
          this.closeScreen()
      }

      this.render().then();
    }

    closeScreen() {
      // delete this.constructor.components[this.nextId];

    }

  }
