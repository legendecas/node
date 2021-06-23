const util = require('util');
let it = new Error('foo');
let item = it;
for (let idx = 0; idx < 2; idx++) {
  item.cause = new Error('bar');
  item = item.cause;
  item.foo = 'bar'
}
console.log(util.format(it));

class Foo extends Error {
  constructor(message, cause) {
    super(message)
    this._cause = cause;
  }

  cause() {
    return this._cause;
  }
}
console.log(util.format(new Foo('foo', new Error('bar'))));
