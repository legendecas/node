'use strict';

// Flag --experimental-vm-modules must not be added.

const common = require('../common');

const assert = require('assert');

const { types } = require('util');
const { Script } = require('vm');

(async () => {
  const script = new Script('globalThis.importResult = import("");', {
    importModuleDynamically: common.mustCall(async () => {
      // Return a ModuleNamespace object without experimental vm modules.
      return import('assert');
    }),
  });
  script.runInThisContext();
  const ns = await globalThis.importResult;
  delete globalThis.importResult;
  assert.ok(types.isModuleNamespaceObject(ns));
})().then(common.mustCall());
