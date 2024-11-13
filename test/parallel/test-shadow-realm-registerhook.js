// Flags: --experimental-shadow-realm

'use strict';

require('../common');
const fixtures = require('../common/fixtures');
const assert = require('assert');

// Test that a ShadowRealm has its own sync loaders, and the loader handles
// import requests of `ShadowRealm.prototype.importValue`.

const resolveHookMod = fixtures.fileURL('es-module-shadow-realm', 'module-hooks/resolve-hook.js');
const stateCounterMod = fixtures.fileURL('es-module-shadow-realm', 'state-counter.mjs');

async function workInChildProcess() {
  const realm = new ShadowRealm();
  const registerHook = await realm.importValue(resolveHookMod, 'register');
  registerHook(resolveHookMod.href);

  // Note that `ShadowRealm.prototype.importValue` has no parent,
  // and it is only valid to import with relative specifier with a custom loader.
  const getCounterInShadowRealm = await realm.importValue('../state-counter.mjs', 'getCounter');
  assert.strictEqual(getCounterInShadowRealm(), 0);
  assert.strictEqual(getCounterInShadowRealm(), 1);

  const { getCounter } = await import(stateCounterMod);
  assert.strictEqual(getCounter(), 0);
}

workInChildProcess();
