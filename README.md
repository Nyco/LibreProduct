# LibreProduct

I am a strategic partner for Free/Libre/OpenSource companies.

Publishers, Integrators, Developers, SaaS, Managed Services, Consulting.

France & Europe.

Fine-tuned your balance between your business models & strategic roadmap, and your communities & ecosystems.

https://libreproduct.tech/

https://fosstodon.org/@nyconyco

## English version

`index.html` (French) is the source of truth. `en/index.html` is generated from it and `i18n/en.json`. After editing either, rebuild:

```sh
python3 scripts/build-en.py          # regenerate en/index.html
python3 scripts/build-en.py --check  # fail if en/index.html is stale
```

New translatable text needs a `data-i18n="key"` attribute in `index.html` and a matching entry in `i18n/en.json`.
