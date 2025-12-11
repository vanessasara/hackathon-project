// Polyfill for crypto.randomUUID (required for HTTP/non-secure contexts)
// This must load before any other scripts
(function() {
  if (typeof crypto !== 'undefined' && !crypto.randomUUID) {
    crypto.randomUUID = function() {
      return '10000000-1000-4000-8000-100000000000'.replace(/[018]/g, function(c) {
        var r = crypto.getRandomValues(new Uint8Array(1))[0];
        return (c ^ (r & (15 >> (c / 4)))).toString(16);
      });
    };
    console.log('crypto.randomUUID polyfill installed');
  }
})();
