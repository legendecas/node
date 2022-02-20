'use strict';

process._rawDebug('main module');
require('internal/modules/cjs/loader');
process._rawDebug('load internal/modules/cjs/loader');
