
import {makeStore } from "./store.js";
import { JsonRpcClient } from "./components/rpc.js";


export async function makeEnvironment() {

  const { core, QWeb, utils } = owl;
  const templates = await utils.loadFile('./xml/app.xml');
  const qweb = new QWeb({templates});
  const bus = new core.EventBus();
  const store = makeStore();
  const rpc = new JsonRpcClient("/rpc");

  return { qweb, bus, store, rpc};

}
