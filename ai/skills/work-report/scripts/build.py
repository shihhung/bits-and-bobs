#!/usr/bin/env python3
"""Compile a standalone report with an existing Tailwind 4 toolchain."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report_dir', type=Path)
    parser.add_argument('--toolchain', type=Path, required=True)
    args = parser.parse_args()
    report = args.report_dir.resolve()
    modules = args.toolchain.resolve() / 'node_modules'
    core = modules / 'tailwindcss'
    cli = modules / '@tailwindcss/cli'
    versions = [json.loads((p / 'package.json').read_text())['version'] for p in (core, cli)]
    if versions[0] != versions[1] or not versions[0].startswith('4.'):
        parser.error('Use matching Tailwind CSS and CLI 4.x versions')
    html = report / 'index.html'
    if not html.is_file():
        parser.error('report_dir must contain index.html')
    source = (report / 'tailwind.input.css').read_text()
    import_line = '@import "tailwindcss" source(none);'
    source_line = '@source "./index.html";'
    if source.count(import_line) != 1 or source.count(source_line) != 1:
        parser.error('Expected the starter import and explicit index.html source directives')
    source = source.replace(import_line, f'@import {json.dumps(str(core / "index.css"))} source(none);')
    source = source.replace(source_line, f'@source {json.dumps(str(html))};')
    # Only replace a previously generated CSS after the compiler succeeds.
    with tempfile.TemporaryDirectory(prefix='work-report-') as scratch:
        temp = Path(scratch)
        input_path = temp / 'input.css'
        output_path = temp / 'style.css'
        input_path.write_text(source)
        subprocess.run(['node', str(cli / 'dist/index.mjs'), '-i', str(input_path),
                        '-o', str(output_path), '--minify'], check=True, cwd=report)
        (report / 'style.css').write_bytes(output_path.read_bytes())
    print(f'Tailwind {versions[0]}: {report / "style.css"}')


if __name__ == '__main__':
    main()
