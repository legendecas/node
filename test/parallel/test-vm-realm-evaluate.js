// Flags: --experimental-vm-realm
'use strict';

require('../common');
const assert = require('node:assert');

const { Realm } = require('node:vm');

const realm = new Realm({
  origin: __filename,
});
assert.ok(realm.globalThis);

realm.evaluate('globalThis.foo = 42');
assert.strictEqual(globalThis.foo, undefined);
assert.strictEqual(realm.globalThis.foo, 42);
assert.strictEqual(realm.evaluate('globalThis.foo'), 42);
