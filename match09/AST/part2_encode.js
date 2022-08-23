(function () {
  var g = function () {
    var p = !![];
    return function (q, r) {
      var u = p ? function () {
        if (r) {
          var y = r["apply"](q, arguments);
          r = null;
          return y;
        }
      } : function () {};
      p = ![];
      return u;
    };
  }();

  var h = g(this, function () {
    var p = function () {
      var q = p["constructor"]("return /\" + this + \"/")()["compile"]("^([^ ]+( +[^ ]+)+)+[^ ]}");
      return !q["test"](h);
    };

    return p();
  });
  h();

  var j = function () {
    var n = !![];
    return function (o, p) {
      var q = n ? function () {
        if (p) {
          var r = p["apply"](o, arguments);
          p = null;
          return r;
        }
      } : function () {};
      n = ![];
      return q;
    };
  }();

  (function () {
    j(this, function () {
      var p = new RegExp("function *\\( *\\)");
      var q = new RegExp("\\+\\+ *(?:[a-zA-Z_$][0-9a-zA-Z_$]*)", "i");
      var r = $c("init");

      if (!p["test"](r + "chain") || !q["test"](r + "input")) {
        r("0");
      } else {
        $c();
      }
    })();
  })();

  var k = function () {
    var p = !![];
    return function (q, r) {
      var u = p ? function () {
        if (r) {
          var v = r["apply"](q, arguments);
          r = null;
          return v;
        }
      } : function () {};
      p = ![];
      return u;
    };
  }();

  var l = k(this, function () {
    var n = function () {};

    var o = function () {
      var s;

      try {
        s = Function("return (function() " + "{}.constructor(\"return this\")( )" + ");")();
      } catch (u) {
        s = window;
      }

      return s;
    };

    var p = o();

    if (!p["console"]) {
      p["console"] = function (s) {
        return t;
      }(n);
    } else {
      p["console"]["log"] = n;
      p["console"]["warn"] = n;
      p["console"]["debug"] = n;
      p["console"]["info"] = n;
      p["console"]["error"] = n;
      p["console"]["exception"] = n;
      p["console"]["table"] = n;
      p["console"]["trace"] = n;
    }
  });
  l();

  try {
    if (global) {
      decrypt("1654614053");
    }
  } catch (o) {
    global = new Array();
  }

  window = new Array();

  for (var m = 0x1; m <= 5; m++) {
    res = decrypt("1654614053") + "r";
  }

  document["cookie"] = "m=" + (m - 0x1)["toString"]() + res + "; path=/";
})();

function $c(b) {
  function e(f) {
    if (typeof f === "string") {
      return function (i) {}["constructor"]("while (true) {}")["apply"]("counter");
    } else {
      if (("" + f / f)["length"] !== 0x1 || f % 0x14 === 0x0) {
        (function () {
          return !![];
        })["constructor"]("debu" + "gger")["call"]("action");
      } else {
        (function () {
          return ![];
        })["constructor"]("debu" + "gger")["apply"]("stateObject");
      }
    }

    e(++f);
  }

  try {
    if (b) {
      return e;
    } else {
      e(0x0);
    }
  } catch (f) {}
}

setInterval(function () {
  $c();
}, 0xfa0);