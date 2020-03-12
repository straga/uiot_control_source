import {initialState} from "./init.js";

const LOCALSTORAGE_KEY = "upy";


const actions = {
    async addSomeData({ state }, records) {
        state[records["state"]] = records["data"];
        },

    async pushSomeData({ state }, records) {
        state[records["state"]].push(records["data"]);

        },

    // async updateSomeData({ state }, records) {
    //     state[records["state"]] = (records["data"]);
    //   },

    async pushTargetData({ state }, records) {
        state[records["state"]][records["target"]].push(records["data"]);
        },

    async updateTargetData({ state }, records) {
        state[records["state"]][records["target"]] = records["data"];
        },

    // async addTargetData({ state }, records) {
    //     state[records["state"]][records["target"]] = (records["data"]);
    //     },



  // async fetchSomeData({ state }, records) {
  //   // const data = await doSomeRPC("/read/", recordId);
  //   // state.recordId = recordId;
  //   // state.recordData = data;
  //     state["state"] = records["data"];
  // },


};

const getters = {

    getTargetData({ state }, records) {
        let _state = false
        if (Object.prototype.hasOwnProperty.call(state, records["state"])){
            let _state = state[records["state"]]
            if (Object.prototype.hasOwnProperty.call(_state, records["target"])){
                _state = _state[records["target"]]
                if (Object.prototype.hasOwnProperty.call(_state, records["data"])){
                    _state = _state[records["data"]]
                }
            }
        }

        return _state
    },

    getSomeData({ state }, records) {
        let _state = false

        if (Object.prototype.hasOwnProperty.call(state, records["state"])){
            _state = state[records["state"]]
                if (Object.prototype.hasOwnProperty.call(_state, records["data"])){
                   _state = _state[records["data"]]
                }
        }

        return _state

    }

    // importantTodoText({ state }, records) {
    //
    //     return state[records["state"]][records["target"]].find(todo => todo.id === records["id"]).text;
    //
    //     },
    //
    // text({ state }, records) {
    //     return state[records["state"]][records["target"]].find(todo => todo.id === records["id"]).text;
    //   }
};





export  function makeStore() {
      function saveState(state) {

          const str = JSON.stringify(state);
          window.localStorage.setItem(LOCALSTORAGE_KEY, str);

      }

      function loadState() {

          const localState = window.localStorage.getItem(LOCALSTORAGE_KEY);

          // return localState ? JSON.parse(localState) : initialState;
          return initialState;
      }

      const state = loadState();

      const store = new owl.Store({ state, actions, getters });

      store.on("update", null, () => saveState(store.state));

      return store;
  }