# Static Tailwind base

Use this only when creating a new page or when the CSS must be rebuilt. Copy `assets/starter/` to the delivery directory, rewrite the sample content, and keep `index.html` and `tailwind.input.css` in the same directory. The CSS is written to `style.css`. The finished page needs neither Node nor a network.

`build.py` uses an existing toolchain. It does not install anything and does not modify the project's package. `--toolchain` points to a directory that contains `node_modules/tailwindcss` and `node_modules/@tailwindcss/cli`, with matching Tailwind 4.x versions. This template was verified with 4.2.1.

```sh
python3 /path/to/work-report/scripts/build.py /path/to/status --toolchain /path/to/existing-toolchain
```

If there is no ready toolchain, install the official pinned versions in a writable, reusable tools directory (replace the path in the example). Do not create a `node_modules` for every report:

```sh
npm install --prefix /path/to/shared-toolchain --no-audit --no-fund --save-exact tailwindcss@4.2.1 @tailwindcss/cli@4.2.1
```

Handle package fetching under your environment's normal authorization. The project's short build note records the real tool versions and the rebuild command. Do not treat a one-time temporary directory as a permanent dependency. The input uses a standard import, and the build helper resolves the tool location only in a temporary copy, leaving the source unchanged.

If a project already has a suitable build, keep using it. Do not force the helper. Official reference: https://tailwindcss.com/docs/installation/tailwind-cli
