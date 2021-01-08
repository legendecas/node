'use strict';
// Flags: --expose-gc

const common = require('../../common');
const binding = require(`./build/${common.buildType}/test_buffer`);
const assert = require('assert');

process.on('uncaughtException', common.mustCall(err => {
  assert.throws(() => { throw err; }, /finalizer error/);
}));

{
  const buffer = binding.malignFinalizerBuffer(common.mustCall(() => {
    throw new Error('finalizer error');
  }));
}
global.gc();
