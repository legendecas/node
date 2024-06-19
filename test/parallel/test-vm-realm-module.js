// Flags: --experimental-vm-realm
'use strict';

const common = require('../common');
const assert = require('node:assert');
const fixtures = require('../common/fixtures');

const { Realm } = require('node:vm');

async function main() {
  const realm = new Realm({
    origin: __filename,
  });
  const mod = fixtures.fileURL('es-module-shadow-realm', 'state-counter.mjs');
  const { getCounter } = await realm.import(mod);
  const { getCounter: getCounter1 } = await realm.import(mod);
  // Verify that the imported values are identical in multiple import.
  assert.strictEqual(getCounter, getCounter1);

  // Verify that the module state is shared between two `importValue` calls.
  assert.strictEqual(getCounter(), 0);
  assert.strictEqual(getCounter1(), 1);
  assert.strictEqual(getCounter(), 2);

  const { getCounter: getCounterThisRealm } = await import(mod);
  assert.notStrictEqual(getCounterThisRealm, getCounter);
  // Verify that the module state is not shared between two realms.
  assert.strictEqual(getCounterThisRealm(), 0);
  assert.strictEqual(getCounter(), 3);
}

main().then(common.mustCall());
