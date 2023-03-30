'use strict';

require('../common');
const assert = require('assert');

function getPrototypeChain(obj) {
  const protos = [];
  let proto;
  do {
    proto = Object.getPrototypeOf(obj);
    obj = proto;
    protos.push(proto);
  } while (proto !== Object && proto != null)
  return protos;
}

const url = new URL('https://nodejs.org');
const insProtos = getPrototypeChain(url);
assert.deepStrictEqual(insProtos, [ URL.prototype, Object.prototype, null ]);
