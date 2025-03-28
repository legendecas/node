// Flags: --resolve-module-cwd=none

'use strict';

const common = require('../common');
const assert = require('node:assert');
const path = require('node:path');
const fixtures = require('../common/fixtures');

const moduleFilepath = fixtures.path('es-modules/imported-esm.mjs');
const dirname = path.dirname(moduleFilepath);

process.chdir(dirname);
// Use indirect `eval` to invoke dynamic `import` without a referrer.
const p = (0, eval)(`import("./imported-esm.mjs")`);
p.then(common.mustCall((ns) => {
  assert.strictEqual(ns.hello, 'world');
}));
