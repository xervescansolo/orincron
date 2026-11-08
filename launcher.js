/**
 * OrinCron — Node.js Launcher
 * Starts the Python bot and auto-restarts it on crash.
 */

const { spawn } = require("child_process");
const path = require("path");

const RESTART_DELAY_MS = 5000;
const MAX_RESTARTS = 10;

let restartCount = 0;
let lastRestartTime = Date.now();

function startBot() {
  console.log(`[OrinCron] Starting bot... (attempt ${restartCount + 1})`);

  const bot = spawn("python", ["orin.py"], {
    cwd: __dirname,
    stdio: "inherit",
    env: { ...process.env },
  });

  bot.on("close", (code) => {
    const now = Date.now();

    // Reset restart counter if it's been more than 60 seconds since last restart
    if (now - lastRestartTime > 60000) {
      restartCount = 0;
    }

    lastRestartTime = now;

    if (code === 0) {
      console.log("[OrinCron] Bot exited cleanly. Not restarting.");
      process.exit(0);
    }

    if (restartCount >= MAX_RESTARTS) {
      console.error(
        `[OrinCron] Reached max restarts (${MAX_RESTARTS}). Giving up.`
      );
      process.exit(1);
    }

    restartCount++;
    console.log(
      `[OrinCron] Bot crashed with code ${code}. Restarting in ${RESTART_DELAY_MS / 1000}s...`
    );

    setTimeout(startBot, RESTART_DELAY_MS);
  });

  bot.on("error", (err) => {
    console.error("[OrinCron] Failed to start bot process:", err.message);
  });

  process.on("SIGINT", () => {
    console.log("[OrinCron] Received SIGINT. Shutting down...");
    bot.kill("SIGINT");
    process.exit(0);
  });

  process.on("SIGTERM", () => {
    console.log("[OrinCron] Received SIGTERM. Shutting down...");
    bot.kill("SIGTERM");
    process.exit(0);
  });
}

startBot();
