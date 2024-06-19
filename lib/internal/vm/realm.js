'use strict';

const {
  emitExperimentalWarning,
  kEmptyObject,
} = require('internal/util');

const {
  ERR_VM_REALM_INVALID_ORIGIN,
} = require('internal/errors').codes;

const {
  VmRealm,
} = internalBinding('contextify');

const { URL } = require('internal/url');
const EventEmitter = require('events');
const { pathToFileURL } = require('url');
const { Script } = require('vm');

let debug = require('internal/util/debuglog').debuglog('vmrealm', (fn) => {
  debug = fn;
});

class Realm extends EventEmitter {
  #wrap = undefined;
  #origin = undefined;

  constructor(options = kEmptyObject) {
    super();
    emitExperimentalWarning('vm.Realm');

    let { origin } = options;

    if (typeof origin === 'string') {
      if (origin.indexOf('file://') === 0) {
        origin = new URL(origin);
      } else {
        origin = pathToFileURL(origin);
      }
    } else if (!(origin instanceof URL)) {
      throw new ERR_VM_REALM_INVALID_ORIGIN(origin);
    }
    this.#origin = origin;

    this.#wrap = new VmRealm();
    // UncaughtException.
    // UnhandledRejection.
  }

  get globalThis() {
    return this.#wrap.globalThis;
  }

  stop() {
    this.#wrap.stop();
  }

  evaluate(script) {
    if (typeof script === 'string') {
      script = new Script(script);
    }
    return this.#wrap.evaluate(script);
  }

  /**
   * @param {string|URL} parentURL
   */
  import(specifier, attributes = kEmptyObject) {
    return this.#wrap.import(`${specifier}`, attributes);
  }
}

module.exports = {
  Realm,
};
