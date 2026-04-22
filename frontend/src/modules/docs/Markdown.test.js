import { describe, expect, it } from "bun:test";
import { marked } from "marked";
import DOMPurify from "dompurify";

describe("Markdown Edge Cases", () => {
  it("should sanitize malicious scripts in markdown", () => {
    const maliciousMd = "# Hello\n\n<script>alert('xss')</script>\n\n[Link](javascript:alert(1))";
    const html = marked.parse(maliciousMd);
    const sanitized = DOMPurify.sanitize(html);
    
    expect(sanitized).not.toContain("<script>");
    expect(sanitized).not.toContain("javascript:alert");
    expect(sanitized).toContain("<h1>Hello</h1>");
  });

  it("should handle deeply nested lists without crashing", () => {
    const nestedMd = "1. a\n  1. b\n    1. c\n      1. d";
    const html = marked.parse(nestedMd);
    expect(html).toContain("<li>a");
  });

  it("should handle empty content", () => {
    const html = marked.parse("");
    expect(html).toBe("");
  });
});
