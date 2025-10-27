#!/usr/bin/env python3

import pathlib
import markdown
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MASTER_MD = ROOT.parent / "Nubu-policies" / "PRIVACY_POLICY.md"
OUTPUT_HTML = ROOT / "nubu-baby" / "privacy.html"
TEMPLATE_PATH = ROOT / "scripts" / "privacy_template.html"

LIST_PATTERN = re.compile(r'<p>([\x010-9].*?)</p>', flags=re.S)


def load_markdown_to_html() -> str:
    text = MASTER_MD.read_text(encoding="utf-8")
    html = markdown.markdown(text, extensions=["extra", "sane_lists"])
    html = fix_numbered_paragraphs(html)
    return html


def fix_numbered_paragraphs(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        content = match.group(1).replace("\x01", "1.")
        lines = [line.strip() for line in content.strip().split("\n") if line.strip()]
        items = []
        for line in lines:
            num_match = re.match(r'(\d+)\.\s*(.*)', line)
            if num_match:
                items.append(num_match.group(2))
        if not items:
            return match.group(0)
        return "<ol>\n" + "\n".join(f"    <li>{item}</li>" for item in items) + "\n</ol>"

    return LIST_PATTERN.sub(repl, html)

def build_document(policy_html: str) -> str:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    return template.replace("{{CONTENT}}", policy_html)

def main():
    policy_html = load_markdown_to_html()
    html_doc = build_document(policy_html)
    OUTPUT_HTML.write_text(html_doc, encoding="utf-8")
    print(f"wrote {OUTPUT_HTML.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
