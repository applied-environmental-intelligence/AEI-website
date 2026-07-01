(function () {
  "use strict";

  /* ---------- Scroll-reveal ---------- */
  var reduce =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealEls = Array.prototype.slice.call(
    document.querySelectorAll("[data-reveal]")
  );
  if (reduce || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) {
      el.classList.add("is-in");
    });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            var el = e.target;
            var d = el.getAttribute("data-reveal-delay");
            if (d) el.style.transitionDelay = d + "ms";
            el.classList.add("is-in");
            io.unobserve(el);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -7% 0px" }
    );
    revealEls.forEach(function (el) {
      io.observe(el);
    });
  }

  /* ---------- Hero cinematic video + geophysical overlay ---------- */
  var hero = document.getElementById("hero");
  var video = document.getElementById("heroVideo");
  var segmentStart = 0;
  var segmentDuration = 15;
  var overlay = document.getElementById("geoOverlay");
  if (!overlay) return;
  var ctx = overlay.getContext("2d");
  if (!ctx) return;
  var W = 0;
  var H = 0;
  var dpr = Math.min(2, window.devicePixelRatio || 1);
  var lowPower =
    (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4) ||
    (navigator.connection && navigator.connection.saveData);
  var targetFps = lowPower ? 24 : 36;
  var frameInterval = 1000 / targetFps;
  var lastFrameAt = 0;
  var rafId = 0;
  var overlayActive = false;
  var heroInView = true;
  var motionEnabled = !reduce;

  var sensors = [
    [0.13, 0.67], [0.22, 0.72], [0.34, 0.66], [0.48, 0.7],
    [0.61, 0.63], [0.76, 0.69], [0.87, 0.61], [0.18, 0.81],
    [0.39, 0.84], [0.58, 0.8], [0.72, 0.83]
  ];

  var agentPaths = [
    { a: 0, b: 3, offset: 0.0 },
    { a: 2, b: 6, offset: 0.22 },
    { a: 7, b: 10, offset: 0.45 },
    { a: 1, b: 8, offset: 0.68 }
  ];

  function resizeOverlay() {
    W = overlay.clientWidth;
    H = overlay.clientHeight;
    dpr = Math.min(2, window.devicePixelRatio || 1);
    overlay.width = Math.floor(W * dpr);
    overlay.height = Math.floor(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function line(x1, y1, x2, y2, alpha, width) {
    ctx.strokeStyle = "rgba(128,245,255," + alpha + ")";
    ctx.lineWidth = width || 1;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }

  function dot(x, y, r, alpha) {
    var g = ctx.createRadialGradient(x, y, 0, x, y, r * 6);
    g.addColorStop(0, "rgba(148,248,255," + alpha + ")");
    g.addColorStop(0.22, "rgba(96,220,255," + alpha * 0.35 + ")");
    g.addColorStop(1, "rgba(96,220,255,0)");
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(x, y, r * 6, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "rgba(220,255,255," + Math.min(1, alpha + 0.2) + ")";
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI * 2);
    ctx.fill();
  }

  function bezier(p0, p1, p2, p3, t) {
    var u = 1 - t;
    return [
      u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
      u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]
    ];
  }

  function drawContours(time) {
    ctx.save();
    ctx.globalAlpha = 0.22;
    ctx.lineWidth = 1;
    for (var j = 0; j < 8; j++) {
      var yBase = H * (0.72 + j * 0.035);
      ctx.strokeStyle = "rgba(118,236,255," + (0.2 - j * 0.012) + ")";
      ctx.beginPath();
      for (var i = 0; i <= 120; i++) {
        var x = W * (i / 120);
        var y = yBase + Math.sin(i * 0.12 + time * 0.55 + j * 0.8) * (6 + j * 1.4) + Math.sin(i * 0.035 + j) * 9;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawWireTerrain(time) {
    ctx.save();
    ctx.globalAlpha = 0.14;
    ctx.strokeStyle = "rgba(128,245,255,0.55)";
    ctx.lineWidth = 1;
    var baseY = H * 0.74;
    var rows = 6;
    for (var r = 0; r < rows; r++) {
      ctx.beginPath();
      for (var i = 0; i <= 80; i++) {
        var x = W * (i / 80);
        var y = baseY + r * H * 0.035 + Math.sin(i * 0.18 + r * 0.7 + time * 0.2) * 4;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
    for (var c = 0; c < 18; c++) {
      var x2 = W * (0.05 + c * 0.055);
      line(x2, baseY - 16, x2 + Math.sin(c) * 24, H * 0.92, 0.08, 1);
    }
    ctx.restore();
  }

  function drawRiskFields(time) {
    ctx.save();
    var cx = W * 0.76;
    var cy = H * 0.55;
    for (var k = 0; k < 5; k++) {
      ctx.strokeStyle = "rgba(140,246,255," + (0.09 + k * 0.018) + ")";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(cx + k * 12, cy + k * 8, 70 + k * 18, 18 + k * 5, -0.22, 0, Math.PI * 2);
      ctx.stroke();
    }
    var gx = W * 0.49;
    var gy = H * 0.77;
    for (var k2 = 0; k2 < 4; k2++) {
      ctx.strokeStyle = "rgba(88,185,255," + (0.11 + 0.02 * Math.sin(time + k2)) + ")";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.ellipse(gx, gy + k2 * 13, 120 + k2 * 30, 22 + k2 * 4, 0.08, 0, Math.PI * 2);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawNetwork(time) {
    var pts = sensors.map(function (s) {
      return [s[0] * W, s[1] * H];
    });
    ctx.save();
    ctx.globalAlpha = 0.65;
    var pairs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [7, 8], [8, 9], [9, 10], [0, 7], [2, 8], [4, 9], [6, 10], [1, 3], [3, 5], [5, 10]];
    pairs.forEach(function (pair, idx) {
      var pulse = 0.07 + 0.06 * (Math.sin(time * 1.2 + idx * 0.9) + 1) / 2;
      line(pts[pair[0]][0], pts[pair[0]][1], pts[pair[1]][0], pts[pair[1]][1], pulse, 1);
    });
    pts.forEach(function (p, idx) {
      dot(p[0], p[1], 2.1 + (idx % 3) * 0.35, 0.5 + 0.22 * Math.sin(time * 1.7 + idx));
    });
    ctx.restore();
  }

  function drawAgents(time) {
    var pts = sensors.map(function (s) {
      return [s[0] * W, s[1] * H];
    });
    ctx.save();
    agentPaths.forEach(function (path, idx) {
      var p0 = pts[path.a];
      var p3 = pts[path.b];
      var midY = Math.min(p0[1], p3[1]) - H * (0.09 + 0.025 * idx);
      var p1 = [p0[0] + (p3[0] - p0[0]) * 0.28, midY];
      var p2 = [p0[0] + (p3[0] - p0[0]) * 0.72, midY + Math.sin(idx) * H * 0.03];
      var u = (time / segmentDuration + path.offset) % 1;
      var pos = bezier(p0, p1, p2, p3, u);
      ctx.strokeStyle = "rgba(128,245,255,0.10)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      for (var s = 0; s <= 30; s++) {
        var p = bezier(p0, p1, p2, p3, s / 30);
        if (s === 0) ctx.moveTo(p[0], p[1]);
        else ctx.lineTo(p[0], p[1]);
      }
      ctx.stroke();
      dot(pos[0], pos[1], 2.7, 0.78);
    });
    ctx.restore();
  }

  function renderOverlay(now) {
    if (!overlayActive) return;
    if (now - lastFrameAt < frameInterval) {
      rafId = requestAnimationFrame(renderOverlay);
      return;
    }
    lastFrameAt = now;
    var time = (now / 1000) % segmentDuration;
    ctx.clearRect(0, 0, W, H);
    drawContours(time);
    drawWireTerrain(time);
    drawRiskFields(time);
    drawNetwork(time);
    drawAgents(time);
    rafId = requestAnimationFrame(renderOverlay);
  }

  function renderStaticOverlay() {
    ctx.clearRect(0, 0, W, H);
    drawContours(0);
    drawWireTerrain(0);
    drawRiskFields(0);
    drawNetwork(0);
    drawAgents(0);
  }

  function stopOverlayLoop() {
    overlayActive = false;
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = 0;
    }
  }

  function startOverlayLoop() {
    if (!motionEnabled || overlayActive) return;
    overlayActive = true;
    rafId = requestAnimationFrame(renderOverlay);
  }

  function syncHeroMotionState() {
    var shouldAnimate = motionEnabled && !document.hidden && heroInView;
    if (video) {
      if (shouldAnimate) {
        video.play().catch(function () {});
      } else {
        video.pause();
      }
    }
    if (shouldAnimate) {
      startOverlayLoop();
    } else {
      stopOverlayLoop();
    }
  }

  if (video) {
    video.addEventListener("loadedmetadata", function () {
      video.currentTime = segmentStart;
      syncHeroMotionState();
    });
    video.addEventListener("timeupdate", function () {
      if (video.currentTime >= segmentStart + segmentDuration) {
        video.currentTime = segmentStart + 0.02;
        if (motionEnabled && !document.hidden && heroInView) {
          video.play().catch(function () {});
        }
      }
    });
  }

  if (hero && "IntersectionObserver" in window) {
    var heroObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          heroInView = entry.isIntersecting;
        });
        syncHeroMotionState();
      },
      { threshold: 0.05 }
    );
    heroObserver.observe(hero);
  }

  document.addEventListener("visibilitychange", syncHeroMotionState, {
    passive: true
  });

  if (reduce) {
    if (video) video.pause();
    renderStaticOverlay();
  }

  resizeOverlay();
  window.addEventListener("resize", resizeOverlay, { passive: true });
  if (!reduce) {
    syncHeroMotionState();
  }
})();
