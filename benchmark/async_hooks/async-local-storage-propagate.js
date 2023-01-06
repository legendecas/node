'use strict';
const common = require('../common.js');
const { AsyncLocalStorage } = require('async_hooks');

/**
 * This benchmark verifies the performance degradation of
 * async resource propagation on the increasing number of
 * active `AsyncLocalStorage`s.
 *
 * - AsyncLocalStorage.run()
 *  - Promise
 *    - Promise
 *      ...
 *        - Promise
 */
const bench = common.createBenchmark(main, {
  storages: [0, 1, 10, 100],
  n: [1e5]
});

function runStores(stores, value, cb, idx = 0) {
  if (idx === stores.length) {
    cb();
  } else {
    stores[idx].run(value, () => {
      runStores(stores, value, cb, idx + 1);
    });
  }
}

async function run(n) {
  for (let i = 0; i < n; i++) {
    await new Promise((resolve) => resolve());
  }
}

function main({ n, storages }) {
  const stores = new Array(storages).fill(0).map(() => new AsyncLocalStorage());
  const contextValue = {};

  runStores(stores, contextValue, () => {
    bench.start();
    run(n).then(() => {
      bench.end(n);
    });
  });
}
