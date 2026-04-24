/* ============================================================
   Google Play Store ML Intelligence System — Client-Side JS
   Features: tsParticles Interactive Background, Typing Animation,
             Animated Counters
   ============================================================ */

(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        initTsParticles();
        setTimeout(function () {
            initTypingAnimation();
            initCounterAnimations();
        }, 600);
    });

    // ═══════════════════════════════════════════════════════════
    //  tsParticles — Interactive Neon Particle Background
    // ═══════════════════════════════════════════════════════════

    function initTsParticles() {
        if (typeof tsParticles === "undefined") {
            setTimeout(initTsParticles, 300);
            return;
        }

        tsParticles.load("tsparticles", {
            fullScreen: false,
            fpsLimit: 120,
            detectRetina: true,

            /* ── Particle properties ── */
            particles: {
                number: {
                    value: 110,
                    density: { enable: true, area: 900 }
                },
                color: {
                    value: ["#00f0ff", "#b44aff", "#3d7aff", "#7c4dff", "#00ff88"]
                },
                shape: { type: "circle" },
                opacity: {
                    value: { min: 0.15, max: 0.65 },
                    animation: {
                        enable: true,
                        speed: 0.8,
                        minimumValue: 0.1,
                        sync: false
                    }
                },
                size: {
                    value: { min: 1, max: 4.5 },
                    animation: {
                        enable: true,
                        speed: 2,
                        minimumValue: 0.5,
                        sync: false
                    }
                },
                shadow: {
                    enable: true,
                    blur: 18,
                    color: "#00f0ff",
                    offset: { x: 0, y: 0 }
                },
                links: {
                    enable: true,
                    distance: 155,
                    color: "#00f0ff",
                    opacity: 0.1,
                    width: 0.8,
                    shadow: {
                        enable: true,
                        blur: 5,
                        color: "#00f0ff"
                    }
                },
                move: {
                    enable: true,
                    speed: { min: 0.3, max: 1.2 },
                    direction: "none",
                    random: true,
                    straight: false,
                    outModes: { default: "out" },
                    attract: {
                        enable: true,
                        rotateX: 600,
                        rotateY: 1200
                    }
                },
                twinkle: {
                    particles: {
                        enable: true,
                        frequency: 0.04,
                        opacity: 1,
                        color: { value: "#ffffff" }
                    }
                }
            },

            /* ── Mouse / touch interaction ── */
            interactivity: {
                detectsOn: "window",
                events: {
                    onHover: {
                        enable: true,
                        mode: ["grab", "bubble"],
                        parallax: {
                            enable: true,
                            force: 50,
                            smooth: 10
                        }
                    },
                    onClick: {
                        enable: true,
                        mode: "repulse"
                    },
                    resize: true
                },
                modes: {
                    grab: {
                        distance: 220,
                        links: {
                            opacity: 0.4,
                            color: "#b44aff"
                        }
                    },
                    bubble: {
                        distance: 200,
                        size: 8,
                        duration: 2,
                        opacity: 0.85,
                        color: { value: "#00f0ff" }
                    },
                    repulse: {
                        distance: 200,
                        duration: 0.6
                    }
                }
            },

            background: { color: "transparent" }
        });
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
            counters.forEach(function (c) { observer.observe(c); });
        } else {
            counters.forEach(animateCounter);
        }
    }
})();
