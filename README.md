# CarvoX Smart Garage Manager

Mobile garage manager (billing, stock, customers, staff, expenses, reports) packaged as an Android app with Capacitor.

## APK kaise banaye (GitHub se)

1. GitHub pe naya repository banao (private bhi chalega).
2. Is zip ke andar ki saari files repository mein upload karo (`.github` folder samet).
3. Repository ke **Actions** tab mein jao. Build apne aap chalega, ya **Build APK** pe click karke **Run workflow** dabao.
4. 4-6 minute baad run khulega, neeche **Artifacts** mein `CarvoX-apk` milega. Download karke zip kholo, andar `app-debug.apk` hai.
5. APK phone mein bhej ke install karo (Unknown sources allow karna padega).

## App badalna

App ka pura code `www/index.html` mein hai. Isme badlav karke push karo, naya APK ban jayega.

## Data

Saara data phone mein hi save hota hai. App uninstall karne se pehle Settings se backup copy kar lena.
