
const { xml } = owl.tags;
const { Component, useState } = owl;
const { useStore, useDispatch} = owl.hooks;
import { HostInfo } from "./device/HostInfo.js";
import { DeviceInfo } from "./device/DeviceInfo.js";
import { MemInfo } from "./device/MemInfo.js";
import { PartitionInfo } from "./device/PartitionInfo.js";
import { BoardInfo } from "./device/BoardInfo.js";

export class StatusTop extends Component {

    static components = {HostInfo, DeviceInfo, MemInfo, PartitionInfo, BoardInfo};

    static template = xml`        
        <div class="bg-light text-dark">
            <div class="screen">
                <div class="container">
                     <HostInfo></HostInfo>
                     <BoardInfo></BoardInfo>
                     <DeviceInfo></DeviceInfo>
                     <MemInfo></MemInfo>
                     <PartitionInfo></PartitionInfo>
                     
                </div>
            </div>
        </div>
    `;








}
