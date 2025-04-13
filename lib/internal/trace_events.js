'use strict';

const { getCategoryEnabledBuffer, trace, usePerfetto } = internalBinding('trace_events');

let nodeTraceEventCategory;
if (usePerfetto) {
  nodeTraceEventCategory = (category) => `${category}`;
} else {
  nodeTraceEventCategory = (category) => `node,${category}`;
}

module.exports = {
  usePerfetto,
  getCategoryEnabledBuffer,
  trace,
  nodeTraceEventCategory,
};
