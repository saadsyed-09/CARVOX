const fs = require('fs');
const path = require('path');

// Clean old build
fs.rmSync('www', { recursive: true, force: true });
fs.mkdirSync('www', { recursive: true });

// Main app
fs.copyFileSync('index.html', 'www/index.html');

// Find a file in any of the usual places
function find(name) {
  const places = [
    path.join('assets', 'assets', name),
    path.join('assets', name),
    name
  ];
  return places.find((p) => fs.existsSync(p));
}

// CarvoX logo -> www/assets/carvox-logo.png (the app shows a built-in logo if this is missing)
const logo = find('carvox-logo.png');
if (logo) {
  fs.mkdirSync('www/assets', { recursive: true });
  fs.copyFileSync(logo, 'www/assets/carvox-logo.png');
  console.log('CarvoX logo copied from ' + logo);
} else {
  console.log('CarvoX logo PNG not found - built-in logo will be used.');
}


// Runtime app logo (header) and invoice logo. Keep both paths available in the WebView.
const appLogo = find('icon.png');
if (appLogo) {
  fs.mkdirSync('www/assets', { recursive: true });
  fs.copyFileSync(appLogo, 'www/assets/icon.png');
  console.log('App icon copied from ' + appLogo);
}

// Optional garage background -> www/garage-bg.png
const bg = find('garage-bg.png');
if (bg) {
  fs.copyFileSync(bg, 'www/garage-bg.png');
  console.log('Background copied from ' + bg);
} else {
  console.log('garage-bg.png not found - plain blue background will be used.');
}

console.log('CarvoX web assets copied to www/');
