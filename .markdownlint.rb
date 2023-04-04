# Config for the markdown linter (used by pre-commit)
# See the following link for more details around why this is used to exclude rules: https://github.com/markdownlint/markdownlint/issues/312
all
exclude_rule 'MD013' # Max line length
exclude_rule 'MD029' # Ordered list item prefix
exclude_rule 'MD033' # Allow Inline HTML
exclude_rule 'MD034' # Bare URL
exclude_rule 'MD036' # Emphasis used instead of a header
