'use strict';
const common = require('../common.js');


const bench = common.createBenchmark(main, {
  n: [10000],
  length: [1, 2, 3, 10, 100],
  kind: ['SumWithIteration', 'SumWithGlobals', 'SumTraditional', 'SumWithTemporaryGlobals', 'SumByNative']
});

function main({ n, length, kind }) {
  let method = process.binding('os')[kind];
  let func;
  if (kind === 'SumByNative') {
    func = function(input) {
      let result = 0;
      for (let i = 0; i < input.length; ++i) {
        result = method(result, input[i])
      }
      return result;
    }
  } else {
    func = method;
  }
  const input = [];
  for (let i = 0; i < length; ++i) {
    input.push(i);
  }
  const output = [];
  for (let i = 0; i < n; ++i) {
    output.push(i);
  }
  bench.start();
  for (let i = 0; i < n; ++i) {
    output[i] = func(input);
  }
  bench.end(n);
}
