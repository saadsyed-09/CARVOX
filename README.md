# CARVOX 4.0 — Capacitor 8 Download + Print build fix

## Why the previous workflow failed
The previous dependency `@capgo/capacitor-file-sharer@^7.0.0` could not be resolved from npm (ETARGET). This pack uses the published Capgo v8 plugin releases and upgrades the Capacitor packages together to v8.

## Replace these files in your GitHub repository
1. `package.json`
2. `.github/workflows/main.yml`

Keep your existing `build.js` as-is. The screenshot shows it correctly copies `index.html` into `www/index.html` and copies the logo/background assets.

## Required existing files
- `index.html` (use your latest CARVOX 4.0 Download/Print HTML)
- `build.js`
- `capacitor.config.ts` with the existing app ID and `webDir: "www"`
- `assets/carvox-logo.png` or `assets/icon.png`

## After committing
1. GitHub → Actions → CARVOX APK → Run workflow.
2. Download the `CARVOX-APK` artifact.
3. Install/test on Android.
4. Test invoice Download and Print on-device.

Note: this pack fixes the dependency/build configuration. It cannot claim the physical APK's print/download behavior is device-tested until you install and test the generated APK.
