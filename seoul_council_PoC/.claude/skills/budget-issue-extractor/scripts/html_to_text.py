#!/usr/bin/env python3
"""예산 원문 HTML을 읽기 쉬운 텍스트로 변환한다.

- 제목(h1~h6)은 '#' 머리표로, 표는 '|' 구분 행으로 보존
- script/style 제거, 연속 공백 정리
- 사용: python3 html_to_text.py input.html [> out.txt]
"""
import sys
from html.parser import HTMLParser

BLOCK = {"p", "div", "section", "article", "li", "br", "tr", "h1", "h2", "h3",
         "h4", "h5", "h6", "table", "details", "summary", "header", "footer"}
SKIP = {"script", "style", "noscript"}


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.buf, self.row = [], [], None
        self.skip = 0
        self.cell = None

    def flush(self):
        text = " ".join("".join(self.buf).split())
        if text:
            self.out.append(text)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
            return
        if tag == "tr":
            self.flush()
            self.row = []
        elif tag in ("td", "th"):
            self.cell = []
        elif tag in BLOCK:
            self.flush()
            if tag[0] == "h" and tag[1:].isdigit():
                self.buf.append("#" * int(tag[1:]) + " ")

    def handle_endtag(self, tag):
        if tag in SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if tag in ("td", "th") and self.cell is not None and self.row is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if any(self.row):
                self.out.append("| " + " | ".join(self.row) + " |")
            self.row = None
        elif tag in BLOCK:
            self.flush()

    def handle_data(self, data):
        if self.skip:
            return
        if self.cell is not None:
            self.cell.append(data)
        else:
            self.buf.append(data)


def main():
    if len(sys.argv) != 2:
        sys.exit("사용법: html_to_text.py input.html")
    with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
        p = Extractor()
        p.feed(f.read())
        p.flush()
    sys.stdout.write("\n".join(p.out) + "\n")


if __name__ == "__main__":
    main()
