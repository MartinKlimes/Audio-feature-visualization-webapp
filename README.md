## Postup, jak to rozchodit:
* Otevřít v PyCharmu složku backend jako projekt a nainstalovat requirements (viz requirements.txt)
* Nainstalovat Node.js a pnpm – https://pnpm.io/installation
* Otevřít ve Visual Studiu Code složku frontend
* Ve VS Code doinstalovat rozšíření 
  * ESLint
  * i18n Ally
  * Iconify IntelliSense
  * Vite
  * Vue Language Features (Volar)
  * WindiCSS IntelliSense
* Ve VS Code spustit konzoli (Ctrl + středník)
* Spustit příkaz pnpm install pro instalaci potřebných Node.js modulů

* Pro vytvoření buildu frontendu, který se zbuildí do složky backend/mos_backend/vue stačí ve VS code spustit příkaz pnpm run build a staré soubory se přemažou novým buildem
* Pro spuštění dev Flask serveru slouží soubor backend/run.py
* Aby fungovala DB, je nutné nejdříve nastavit v backend/mos\_backend/\_\_init\_\_.py správnou DB URI
* Po nastavení DB URI je nutné spustit skript create\_tables.py, který vytvoří tabulku s uživateli (dělá se jenom jednou)
* Následně je možné se skrze aplikaci zaregistrovat a přihlásit
