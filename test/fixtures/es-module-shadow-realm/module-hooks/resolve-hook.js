import { registerHooks } from 'node:module';

export function register(origin) {
  function resolve(specifier, context, nextResolve) {
    if (context.parentURL === undefined) {
      // Handles `ShadowRealm.prototype.importValue` which has no `parentURL`.
      return nextResolve(specifier, {
        ...context,
        parentURL: origin,
      });
    }
    return nextResolve(specifier, context);
  }

  registerHooks({ resolve });
}
