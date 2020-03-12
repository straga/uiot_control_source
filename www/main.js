
import { makeEnvironment } from "./env.js";
import { App } from "./components/App.js";
import { ResponsivePlugin } from "./components/Tools.js";


function main() {


    //------------------------------------------------------------------------------
    // Debug
    //--------

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

    ResponsivePlugin(App.env);

    const app = new App();
    app.mount(document.body);

}

async function start() {
    owl.config.mode = "dev";

    const env = await makeEnvironment();

    owl.Component.env = env;
    await owl.utils.whenReady();
    main();
}

start();
