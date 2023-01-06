'use strict';
const common = require('../common.js');
const { AsyncLocalStorage } = require('async_hooks');

/**
 * This benchmark verifies the performance degradation of
 * `AsyncLocalStorage.getStore()` on propagation through deep async
 * resource turns.
 *
 * - AsyncLocalStorage.run()
 *  - Promise
 *    - Promise
 *      ...
 *        - Promise
 *          - AsyncLocalStorage.getStore()
 */
const bench = common.createBenchmark(main, {
  turns: [1, 10, 100],
  n: [1e4]
});

function run(store, n, turns) {
  let promises = [];
  for (let i = 0; i < n; i++) {
    promises.push(store.run(i, () => doRun(store, turns)));
  }
  return Promise.all(promises);
}

function doRun(store, turns) {
  let promise = Promise.resolve();
  for (let i = 0; i < turns; i++) {
    promise = promise.then(() => {
      return Promise.resolve();
    });
  }
  return promise.then(() => store.getStore());
}

function main({ n, turns }) {
  const store = new AsyncLocalStorage();
  bench.start();
  run(store, n, turns).then(() => {
    bench.end(n);
  });
}
