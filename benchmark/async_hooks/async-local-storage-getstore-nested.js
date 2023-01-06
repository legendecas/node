'use strict';
const common = require('../common.js');
const { AsyncLocalStorage } = require('async_hooks');

/**
 * This benchmark verifies the performance degradation of
 * `AsyncLocalStorage.getStore()` on multiple `AsyncLocalStorage` instances
 * nested `AsyncLocalStorage.run()`s.
 *
 * - AsyncLocalStorage1.run()
 *   - AsyncLocalStorage2.run()
 *    ...
 *      - AsyncLocalStorageN.run()
 *        - AsyncLocalStorage1.getStore()
 */
const bench = common.createBenchmark(main, {
  turns: [1, 10, 100],
  n: [1e4]
});

function run(stores, value, n) {
  for (let idx = 0; idx < n; idx++) {
    runStores(stores, value);
  }
}

function runStores(stores, value, idx = 0) {
  if (idx === stores.length) {
    stores[0].getStore();
  } else {
    stores[idx].run(value, () => {
      runStores(stores, value, idx + 1);
    });
  }
}

function main({ n, turns }) {
  const stores = new Array(turns).fill(0).map(() => new AsyncLocalStorage());
  const contextValue = {};

  bench.start();
  run(stores, contextValue, n);
  bench.end(n);
}
