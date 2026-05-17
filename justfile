# Justfile for inflecv
# Modern command runner for build automation.
#
# Customise `cv_name` in a local override (`.justfile.local`) or via
# environment: `just cv_name=CV-Jane-Smith-2026 build`.

# CV output name with year-month (sample: John Doe)
cv_name := env_var_or_default("CV_NAME", "CV-John-Doe-" + `date +%Y-%m`)

# Default recipe (runs when you type `just`)
default: build

# Build the CV (default: full version)
build:
    @echo "Building CV..."
    @mkdir -p dist
    typst compile src/cv.typ dist/{{cv_name}}.pdf
    @echo "✓ Built dist/{{cv_name}}.pdf"

# Watch for changes and rebuild automatically
watch:
    @echo "Watching for changes..."
    @mkdir -p dist
    typst watch src/cv.typ dist/{{cv_name}}.pdf

# Lint everything (Python + Markdown)
lint:
    @uv run --extra dev ruff check scripts/
    @command -v markdownlint >/dev/null && markdownlint '**/*.md' || echo "(markdownlint not installed; skipping)"

# Format Python sources
format:
    @uv run --extra dev ruff format scripts/

# Clean build artifacts
clean:
    @echo "Cleaning build artifacts..."
    @rm -rf dist/*.pdf
    @echo "✓ Cleaned"

# Build adapted CV for a specific application (slug naming convention)
build-adapted app_id:
    @echo "Building adapted CV for {{app_id}}..."
    @mkdir -p data/applications/{{app_id}}
    typst compile --root . data/applications/{{app_id}}/{{app_id}}-cv-adapted.typ data/applications/{{app_id}}/{{app_id}}-cv-adapted.pdf
    @echo "✓ Built data/applications/{{app_id}}/{{app_id}}-cv-adapted.pdf"

# Validate CV compiles without errors
validate:
    @echo "Validating CV..."
    @typst compile src/cv.typ --diagnostic-format=short > /dev/null 2>&1 && echo "✓ Validation passed" || (echo "✗ Validation failed" && exit 1)

# Run all verification scripts (Python)
verify:
    @uv run python -m scripts.verification

# Run verification with specific check
verify-build:
    @uv run python -m scripts.verification --build

verify-dates:
    @uv run python -m scripts.verification --dates

verify-format:
    @uv run python -m scripts.verification --format

# Run verification tests
test-verify:
    @uv run --extra dev pytest scripts/verification/tests/ -v

# Run all tests with coverage
test:
    @uv run --extra dev pytest scripts/ -v --cov=scripts --cov-report=term-missing

# Run mutation testing on lib/
test-mutate:
    @uv run --extra dev mutmut run

# Show mutation testing results
test-mutate-results:
    @uv run --extra dev mutmut results

# Show available recipes
list:
    @just --list
