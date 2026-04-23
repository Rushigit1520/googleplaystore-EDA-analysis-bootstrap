/* ============================================================
   Google Play Store ML Intelligence System — Client-Side JS
   Features: Particle Background, Typing Animation, Counters
   ============================================================ */

(function () {
    "use strict";

    // ─── Wait for DOM ──────────────────────────────────────────
    document.addEventListener("DOMContentLoaded", function () {
        initParticles();
        // Dash takes a moment to render; wait a bit then init animations
        setTimeout(function () {
            initTypingAnimation();
            initCounterAnimations();
        }, 600);
    });

    // ═══════════════════════════════════════════════════════════
    //  PARTICLE BACKGROUND — Vanilla JS (no external lib)
    // ═══════════════════════════════════════════════════════════
    function initParticles() {
        var canvas = document.getElementById("particle-canvas");
        if (!canvas) return;
        var ctx = canvas.getContext("2d");

        var particles = [];
        var PARTICLE_COUNT = 80;
        var CONNECTION_DIST = 140;
        var mouse = { x: null, y: null };

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener("resize", resize);

        document.addEventListener("mousemove", function (e) {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });
        document.addEventListener("mouseleave", function () {
            mouse.x = null;
            mouse.y = null;
        });

        // Create particles
        for (var i = 0; i < PARTICLE_COUNT; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.6,
                vy: (Math.random() - 0.5) * 0.6,
                radius: Math.random() * 2 + 0.8,
                color: ["#00f0ff", "#b44aff", "#ff2d95", "#00ff88", "#3d7aff"][
                    Math.floor(Math.random() * 5)
                ],
                alpha: Math.random() * 0.5 + 0.3,
            });
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (var i = 0; i < particles.length; i++) {
                var p = particles[i];

                // Move
                p.x += p.vx;
                p.y += p.vy;

                // Bounce
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

                // Draw dot
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.globalAlpha = p.alpha;
                ctx.fill();
                ctx.globalAlpha = 1;

                // Connect nearby particles
                for (var j = i + 1; j < particles.length; j++) {
                    var q = particles[j];
                    var dx = p.x - q.x;
                    var dy = p.y - q.y;
                    var dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < CONNECTION_DIST) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(q.x, q.y);
                        ctx.strokeStyle = p.color;
                        ctx.globalAlpha = 0.08 * (1 - dist / CONNECTION_DIST);
                        ctx.lineWidth = 0.6;
                        ctx.stroke();
                        ctx.globalAlpha = 1;
                    }
                }

                // Mouse attraction
                if (mouse.x !== null) {
                    var mdx = mouse.x - p.x;
                    var mdy = mouse.y - p.y;
                    var mDist = Math.sqrt(mdx * mdx + mdy * mdy);
                    if (mDist < 200) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(mouse.x, mouse.y);
                        ctx.strokeStyle = var_neonCyan;
                        ctx.globalAlpha = 0.06 * (1 - mDist / 200);
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                        ctx.globalAlpha = 1;
                    }
                }
            }

            requestAnimationFrame(animate);
        }

        var var_neonCyan = "#00f0ff";
        animate();
    }

    // ═══════════════════════════════════════════════════════════
    //  TYPING ANIMATION
    // ═══════════════════════════════════════════════════════════
    function initTypingAnimation() {
        var el = document.getElementById("typing-text");
        if (!el) return;

        var fullText = el.getAttribute("data-text");
        if (!fullText) return;

        el.textContent = "";
        var index = 0;

        function typeChar() {
            if (index < fullText.length) {
                el.textContent += fullText.charAt(index);
                index++;
                setTimeout(typeChar, 55 + Math.random() * 40);
            }
        }

        typeChar();
    }

    // ═══════════════════════════════════════════════════════════
    //  ANIMATED COUNTERS (with IntersectionObserver)
    // ═══════════════════════════════════════════════════════════
    function initCounterAnimations() {
        var counters = document.querySelectorAll(".counter-value");
        if (!counters.length) return;

        function animateCounter(el) {
            var target = parseFloat(el.getAttribute("data-target"));
            if (isNaN(target)) return;
            var decimals = parseInt(el.getAttribute("data-decimals") || "0", 10);
            var suffix = el.getAttribute("data-suffix") || "";
            var duration = 2000;
            var startTime = null;

            function step(timestamp) {
                if (!startTime) startTime = timestamp;
                var progress = Math.min((timestamp - startTime) / duration, 1);
                // ease-out cubic
                var eased = 1 - Math.pow(1 - progress, 3);
                var current = eased * target;

                if (decimals > 0) {
                    el.textContent = current.toFixed(decimals) + suffix;
                } else {
                    el.textContent = Math.floor(current).toLocaleString() + suffix;
                }

                if (progress < 1) {
                    requestAnimationFrame(step);
                } else {
                    if (decimals > 0) {
                        el.textContent = target.toFixed(decimals) + suffix;
                    } else {
                        el.textContent = target.toLocaleString() + suffix;
                    }
                }
            }

            requestAnimationFrame(step);
        }

        if ("IntersectionObserver" in window) {
            var observer = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            animateCounter(entry.target);
                            observer.unobserve(entry.target);
                        }
                    });
                },
                { threshold: 0.3 }
            );
            counters.forEach(function (c) {
                observer.observe(c);
            });
        } else {
            counters.forEach(animateCounter);
        }
    }
})();
