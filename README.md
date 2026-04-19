# ml-engineering-slides

Slide decks for AIOS team meetings. Each presentation lives in its own directory named `MM-DD-YYYY/`.

## Creating a new presentation

Use the `/aios-slides` slash command in Claude Code. It will create a new dated directory and generate slides there.

## Directory structure

```
MM-DD-YYYY/
  context.md           # prompt / brief given to Claude
  presentation-plan.md # slide plan
  gen_slides.py        # slide generation script
  assemble_pptx.py     # PPTX assembly script
  requirements.txt     # Python dependencies
  *.py                 # diagram generators
```

Generated outputs (`*.png`, `*.pptx`, `*.docx`) are excluded from git — re-run the scripts to regenerate.

## Cleaning generated files

```bash
./clean.sh           # remove *.png, *.pptx, *.docx, __pycache__
./clean.sh --venv    # also remove .venv directories
```

## Running scripts

A shared virtual environment is used across all presentations:

```bash
cd MM-DD-YYYY/
source ~/.claude/venvs/aios-slides/bin/activate
python gen_slides.py
```

If a new package is needed, install it into the shared venv:

```bash
source ~/.claude/venvs/aios-slides/bin/activate && pip install <package>
```
