// Flags: --resolve-module-cwd=throw

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
assert.rejects(p, {
  code: 'ERR_INVALID_RELATIVE_MODULE_SPECIFIER',
}).then(common.mustCall());
