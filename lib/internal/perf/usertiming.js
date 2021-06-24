'use strict';

const {
  ObjectSetPrototypeOf,
  SafeMap,
  SafeSet,
  SafeArrayIterator,
  SymbolToStringTag,
  TypeError,
} = primordials;

const { InternalPerformanceEntry } = require('internal/perf/performance_entry');
const { now } = require('internal/perf/utils');
const { enqueue } = require('internal/perf/observe');
const nodeTiming = require('internal/perf/nodetiming');

const {
  validateNumber,
  validateObject,
  validateString,
} = require('internal/validators');

const {
  codes: {
    ERR_INVALID_ARG_VALUE,
    ERR_PERFORMANCE_INVALID_TIMESTAMP,
    ERR_PERFORMANCE_MEASURE_INVALID_OPTIONS,
  },
} = require('internal/errors');

const { structuredClone, lazyDOMException } = require('internal/util');

const markTimings = new SafeMap();

const nodeTimingReadOnlyAttributes = new SafeSet(new SafeArrayIterator([
  'nodeStart',
  'v8Start',
  'environment',
  'loopStart',
  'loopExit',
  'bootstrapComplete',
]));

function getMark(name) {
  if (name === undefined) return;
  if (typeof name === 'number') {
    if (name < 0)
      throw new ERR_PERFORMANCE_INVALID_TIMESTAMP(name);
    return name;
  }
  name = `${name}`;
  if (nodeTimingReadOnlyAttributes.has(name))
    return nodeTiming[name];
  const ts = markTimings.get(name);
  if (ts === undefined)
    throw lazyDOMException(`The "${name}" performance mark has not been set`, 'SyntaxError');
  return ts;
}

// A valid PerformanceMeasureOptions should contains one of the properties.
function isValidStartOrMeasureOptions(options) {
  return typeof options === 'object' &&
    (options.start !== undefined ||
    options.end !== undefined ||
    options.duration !== undefined ||
    options.detail !== undefined);
}

class PerformanceMark extends InternalPerformanceEntry {
  constructor(name, options) {
    name = `${name}`;
    if (nodeTimingReadOnlyAttributes.has(name))
      throw new ERR_INVALID_ARG_VALUE('name', name);
    options ??= {};
    validateObject(options, 'options');
    const startTime = options.startTime ?? now();
    validateNumber(startTime, 'startTime');
    if (startTime < 0)
      throw new ERR_PERFORMANCE_INVALID_TIMESTAMP(startTime);
    markTimings.set(name, startTime);

    const detail = options.detail != null ?
      structuredClone(options.detail) :
      null;
    super(name, 'mark', startTime, 0, detail);
  }

  get [SymbolToStringTag]() {
    return 'PerformanceMark';
  }
}

class PerformanceMeasure extends InternalPerformanceEntry {
  constructor() {
    // eslint-disable-next-line no-restricted-syntax
    throw new TypeError('Illegal constructor');
  }

  get [SymbolToStringTag]() {
    return 'PerformanceMeasure';
  }
}

class InternalPerformanceMeasure extends InternalPerformanceEntry {
  constructor(name, start, duration, detail) {
    super(name, 'measure', start, duration, detail);
  }
}

InternalPerformanceMeasure.prototype.constructor =
  PerformanceMeasure.prototype.constructor;
ObjectSetPrototypeOf(InternalPerformanceMeasure.prototype,
                     PerformanceMeasure.prototype);

function mark(name, options = {}) {
  const mark = new PerformanceMark(name, options);
  enqueue(mark);
  return mark;
}

function calculateStartDuration(startOrMeasureOptions, endMark) {
  startOrMeasureOptions ??= 0;
  let start;
  let end;
  const optionsValid = isValidStartOrMeasureOptions(startOrMeasureOptions);
  if (optionsValid) {
    if (endMark !== undefined) {
      throw new ERR_PERFORMANCE_MEASURE_INVALID_OPTIONS(
        'endMark must not be specified');
    }
    if (!(startOrMeasureOptions.start !== undefined) &&
      !(startOrMeasureOptions.end !== undefined)) {
      throw new ERR_PERFORMANCE_MEASURE_INVALID_OPTIONS(
        'One of options.start or options.end is required');
    }
    if (startOrMeasureOptions.start !== undefined &&
      startOrMeasureOptions.end !== undefined &&
      startOrMeasureOptions.duration !== undefined) {
      throw new ERR_PERFORMANCE_MEASURE_INVALID_OPTIONS(
        'Must not have options.start, options.end, and ' +
        'options.duration specified');
    }
  }

  if (endMark !== undefined) {
    end = getMark(endMark);
  } else if (optionsValid && startOrMeasureOptions.end !== undefined) {
    end = getMark(startOrMeasureOptions.end);
  } else if (optionsValid &&
    startOrMeasureOptions.start !== undefined &&
    startOrMeasureOptions.duration !== undefined) {
    end = getMark(startOrMeasureOptions.start) +
      getMark(startOrMeasureOptions.duration);
  } else {
    end = now();
  }

  if (optionsValid && startOrMeasureOptions.start !== undefined) {
    start = getMark(startOrMeasureOptions.start);
  } else if (optionsValid &&
    startOrMeasureOptions.duration !== undefined &&
    startOrMeasureOptions.end !== undefined) {
    start = getMark(startOrMeasureOptions.end) -
      getMark(startOrMeasureOptions.duration);
  } else if (typeof startOrMeasureOptions === 'string') {
    start = getMark(startOrMeasureOptions);
  } else {
    start = 0;
  }

  const duration = end - start;

  return { start, duration };
}

function measure(name, startOrMeasureOptions, endMark) {
  validateString(name, 'name');
  const {
    start,
    duration,
  } = calculateStartDuration(startOrMeasureOptions, endMark);
  let detail = startOrMeasureOptions?.detail;
  detail = detail != null ? structuredClone(detail) : null;
  const measure = new InternalPerformanceMeasure(name, start, duration, detail);
  enqueue(measure);
  return measure;
}

function clearMarkTimings(name) {
  if (name !== undefined) {
    name = `${name}`;
    if (nodeTimingReadOnlyAttributes.has(name))
      throw new ERR_INVALID_ARG_VALUE('name', name);
    markTimings.delete(name);
    return;
  }
  markTimings.clear();
}

module.exports = {
  PerformanceMark,
  PerformanceMeasure,
  clearMarkTimings,
  mark,
  measure,
};
