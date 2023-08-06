docstring_quotes = ["'''", '"""']
ignore_list_global = ["__pycache__", ".DS_Store"]
declaration_regex = r"(?:class|def)\s+\w+\s*(?:\(\s*[\"((\w|\".\")\s:,\"'*=\[\]]*\))?\s*(?:->\s*(?:\"?(?:\w(?:\.)?)+\"?)(?:\[[\w\s:,.\"\[\]]*\]\s*)?\s*)?:([ \t]*#.*?(?=\n))?\n"
end_of_declaration_regex = r":[ \t\r\f\v]*(?:#.*?(?=\n))?\n"
