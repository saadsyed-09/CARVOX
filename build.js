const fs = require("fs");
const path = require("path");

const root = __dirname;
const www = path.join(root, "www");
const source = path.join(root, "index.html");

if (!fs.existsSync(source)) {
  throw new Error("Missing index.html in project root.");
}

fs.rmSync(www, { recursive: true, force: true });
fs.mkdirSync(www, { recursive: true });
fs.copyFileSync(source, path.join(www, "index.html"));

const assets = path.join(root, "assets");
if (fs.existsSync(assets)) {
  fs.cpSync(assets, path.join(www, "assets"), { recursive: true });
}

// Optional local wallpaper; the app falls back gracefully if absent.
const wallpaper = path.join(root, "garage-bg.png");
if (fs.existsSync(wallpaper)) {
  fs.copyFileSync(wallpaper, path.join(www, "garage-bg.png"));
}

console.log("CarvoX web files prepared in www/");
