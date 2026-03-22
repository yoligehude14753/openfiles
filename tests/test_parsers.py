import pytest
from pathlib import Path

from src.parsers import ParserFactory
from src.parsers.text_parser import TextParser
from src.parsers.markdown_parser import MarkdownParser


class TestParserFactory:
    def test_get_parser_txt(self):
        factory = ParserFactory()
        parser = factory.get_parser("txt")
        assert isinstance(parser, TextParser)

    def test_get_parser_md(self):
        factory = ParserFactory()
        parser = factory.get_parser("md")
        assert isinstance(parser, MarkdownParser)

    def test_get_parser_unknown(self):
        factory = ParserFactory()
        parser = factory.get_parser("zzz_unknown")
        assert parser is None

    def test_parse_file_unknown_type(self, tmp_path):
        factory = ParserFactory()
        result = factory.parse_file(tmp_path / "test.zzz", "zzz")
        assert result["success"] is False
        assert "No parser available" in result["error"]

    def test_supported_types_not_empty(self):
        factory = ParserFactory()
        types = factory.supported_types()
        assert len(types) > 0
        assert "txt" in types
        assert "pdf" in types


class TestTextParser:
    def test_parse_basic(self, sample_text_file):
        parser = TextParser()
        result = parser.parse(sample_text_file)
        assert result["success"] is True
        assert "Hello, world!" in result["content"]
        assert result["line_count"] == 3
        assert result["char_count"] > 0

    def test_parse_nonexistent(self, tmp_path):
        parser = TextParser()
        result = parser.parse(tmp_path / "nope.txt")
        assert result["success"] is False
        assert result["content"] == ""

    def test_can_parse_supported(self):
        parser = TextParser()
        assert parser.can_parse("txt") is True
        assert parser.can_parse("py") is True
        assert parser.can_parse("js") is True
        assert parser.can_parse("json") is True

    def test_can_parse_unsupported(self):
        parser = TextParser()
        assert parser.can_parse("pdf") is False
        assert parser.can_parse("docx") is False


class TestMarkdownParser:
    def test_parse_with_frontmatter(self, sample_markdown_file):
        parser = MarkdownParser()
        result = parser.parse(sample_markdown_file)

        assert result["success"] is True
        assert result["frontmatter"]["title"] == "Test Doc"
        assert result["frontmatter"]["author"] == "OpenFiles"
        assert "Heading One" not in result.get("frontmatter", {})

    def test_headings_extracted(self, sample_markdown_file):
        parser = MarkdownParser()
        result = parser.parse(sample_markdown_file)

        headings = result["headings"]
        assert len(headings) == 2
        assert headings[0]["text"] == "Heading One"
        assert headings[1]["text"] == "Heading Two"

    def test_links_extracted(self, sample_markdown_file):
        parser = MarkdownParser()
        result = parser.parse(sample_markdown_file)

        links = result["links"]
        assert len(links) == 1
        assert links[0]["url"] == "https://example.com"

    def test_no_frontmatter(self, tmp_path):
        p = tmp_path / "plain.md"
        p.write_text("# Just a heading\n\nSome text.")
        parser = MarkdownParser()
        result = parser.parse(p)

        assert result["success"] is True
        assert result["frontmatter"] == {}
        assert "Just a heading" in result["content"]
