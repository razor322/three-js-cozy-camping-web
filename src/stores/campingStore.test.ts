import { strict as assert } from "node:assert";
import { useCampingStore, objectInfo } from "./campingStore.ts";

const s = () => useCampingStore.getState();

s().setPhotoMode(true);
assert.equal(s().photoMode, true, "setPhotoMode(true) sets photoMode");
s().setPhotoMode(false);
assert.equal(s().photoMode, false, "setPhotoMode(false) clears photoMode");

const before = s().tentOpen;
s().toggleTent();
assert.equal(s().tentOpen, !before, "toggleTent flips tentOpen");
s().toggleTent();

assert.equal(typeof objectInfo.campfire.status, "string", "campfire has a status line");
assert.ok(Array.isArray(objectInfo.tent.facts) && objectInfo.tent.facts.length > 0, "tent has facts");
assert.ok(objectInfo.lantern.facts.length > 0, "lantern has facts");

console.log("campingStore: all checks passed");
