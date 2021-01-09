import { BigInteger as BigInt } from 'jsbn';

// why not?
// ZERO AND ONE are already taken care of
BigInt.TWO = new BigInt('2', 10);

BigInt.setup = function(callback, fail_callback) {
    // nothing to do but go
    callback();
};

BigInt.prototype.toJSONObject = function() {
    return this.toString();
};

BigInt.fromJSONObject = function(s) {
    return new BigInt(s, 10);
};

BigInt.fromInt = function(i) {
    return BigInt.fromJSONObject('' + i);
};

BigInt.use_applet = false;
/* jshint ignore:end */

export { BigInt };