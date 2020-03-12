import { Home } from "./screen/home.js";
import { WiFi } from "./screen/wifi.js";
import { System } from "./screen/system.js";
import { OTA } from "./screen/ota.js";
import { Device } from "./screen/device.js";
import { Hardware } from "./screen/hw.js";


export const initialState =
    {
        menus: [
                { id:1, key: "home",name: "Home", parent: false, action: "screen" },
                { id:2, key: "wifi", name: "Wifi", parent: false, action: "screen"},
                { id:4, key: "scan",name: "Scan", parent: 'wifi', action: "func" },
                { id:5, key: "ap",name: "AP", parent: 'wifi', action: "func" },
                { id:6, key: "station",name: "Station", parent: 'wifi', action: "func" },
                { id:3, key: "system", name: 'System', parent: false, action: "screen"},
                { id:7, key: "restart", name: 'Restart', parent: "system", action: "func"},
                { id:8, key: "tables", name: 'Tables', parent: "system", action: "func"},
                { id:10, key: "ota", name: 'OTA', parent: false, action: "screen"},
                { id:11, key: "ota_manual", name: 'Update', parent: "ota", action: "func"},
                { id:12, key: "ota_client", name: 'Client', parent: "ota", action: "func"},
                { id:13, key: "ota_server", name: 'Server', parent: "ota", action: "func"},
                { id:14, key: "devices", name: 'Devices', parent: false, action: "screen"},
                { id:15, key: "devices_connect", name: 'Connect', parent: "devices", action: "func"},
                { id:15, key: "devices_list", name: 'List', parent: "devices", action: "func"},
                { id:14, key: "hw", name: 'Hardware', parent: false, action: "screen"},
                { id:15, key: "hw_pin_value", name: 'Pin Value', parent: "hw", action: "func"},
          ],
        nextId: 15,

        srceensViews:[
            {name: "home", screen: Home},
            {name: "wifi", screen: WiFi},
            {name: "system", screen: System},
            {name: "ota", screen: OTA},
            {name: "device", screen: Device},



        ],

        screensList: [
            {
              name: "home",
              title: "Home",
              component: Home,
            },

            {
              name: "wifi",
              title: "WiFi",
              component: WiFi,
            },
            {
              name: "system",
              title: "System",
              component: System,
            },
            {
              name: "ota",
              title: "ota",
              component: OTA,
            },
            {
              name: "devices",
              title: "Devices",
              component: Device,
            },

            {
              name: "hw",
              title: "Hardware",
              component: Hardware,
            }

            ],
        modelDB: [


        ]
    }

;





//   export const initialState = {
//       menus: [
//           { id:1, key: "home",name: "Home" },
//           { id:2, key: "wifi", name: "Wifi"},
//           { id:3, key: "system", name: 'System'}
//           ],
//       nextId: 4};
//
//
// export const ROUTES = [
//   { name: "LANDING", path: "/", component: Landing },
//   { name: "SIGN_UP", path: "/signup", component: SignUp },
//   { name: "SIGN_IN", path: "/signin", component: SignIn },
//   { name: "PASSWORD_FORGET", path: "/pw-forget", component: PasswordForget },
//   {
//     name: "HOME",
//     path: "/home",
//     component: Home,
//     beforeRouteEnter: protectRoute
//   },
//   {
//     name: "ADMIN",
//     path: "/admin",
//     component: Admin,
//     beforeRouteEnter: protectRoute
//   },
//   {
//     name: "ACCOUNT",
//     path: "/account",
//     component: Account,
//     beforeRouteEnter: protectRoute
//   },
//   {
//     name: "UNKNOWN",
//     path: "*",
//     redirect: { to: "LANDING" }
//   }
// ];