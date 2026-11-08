# CarvoX Android project

## Build APK with GitHub Actions
1. Upload the contents of this ZIP to your GitHub repository (keep `.github/workflows/main.yml`).
2. Commit/push to `main` or `master`, or open **Actions → Build CarvoX Android APK → Run workflow**.
3. After the workflow completes, download the `CarvoX-debug-apk` artifact.

## Project notes
- `index.html` is the uploaded CarvoX HTML source. It is copied into `www/index.html` by `build.js`.
- The app's existing HTML design and code were preserved; no UI redesign was applied.
- The HTML references `assets/carvox-logo.png` and optional `garage-bg.png`. If you have your exact logo/wallpaper files, add them at those paths. Without them, the HTML's built-in fallback logo is used.
- Capacitor app ID is retained as `com.garagemanager.app` to avoid changing the app identity.
- This workflow builds a **debug APK**. It has not been signed as a release APK.
