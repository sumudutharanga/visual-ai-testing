# Visual AI Testing Framework

An AI-powered Visual UI Testing Framework built with **Python**, **Playwright**, **OpenCV**, **Figma JSON**, **n8n**, and **Jira**.

This framework automatically compares a live website against a Figma design, validates UI components, analyzes visual and CSS differences, generates an HTML report, and creates Jira bug tickets automatically.

---

# Features

## Visual Testing

- Compare Figma design with live website
- OpenCV image comparison
- Highlight visual differences
- Pixel tolerance support (ignore ≤1px differences)

## Component Validation

- Component-based testing using data-testid
- DOM validation
- CSS validation
- Layout validation

## Typography Validation

- Font Size
- Font Weight
- Font Family
- Line Height
- Text Content

## Style Validation

- Text Color
- Background Color
- Border Radius
- Padding
- Margin
- Width
- Height

## Reporting

- JSON Reports
- HTML Dashboard
- Visual Difference Images
- AI-generated explanations
- Suggested fixes
- Severity levels

## Jira Automation

- Automatic Jira Bug Creation
- n8n Integration
- One ticket per failed component

---

# 🛠 Tech Stack

- Python 3.12+
- Playwright
- OpenCV
- Pillow
- NumPy
- Figma JSON Export
- n8n
- Jira Cloud
- HTML

---

# 📂 Project Structure

```
visual-ai-testing/

config/
    settings.py

data/
    urls.py
    figma_component_map.json

expected/
    upload_modal.json

figma/
    expected/
        upload_modal.png
    figma_export.json

reports/
    ai/
    components/
    css/
    dom/
    final/
    jira/
    layout/
    validation/
    difference.png
    highlighted.png

screenshots/
    actual.png
    components/

templates/
    report.html

test/
    main.py
    compare.py
    component_capture.py
    screenshot_capture.py

utils/
    ai_analyzer.py
    component_analyzer.py
    css_reader.py
    dom_reader.py
    figma_json_parser.py
    final_report_builder.py
    html_report.py
    image_compare.py
    jira_payload_builder.py
    layout_reader.py
    n8n_client.py
    validator.py

.env.example
README.md
requirements.txt
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/visual-ai-testing.git
```

Open the project

```bash
cd visual-ai-testing
```

Create virtual environment

Linux

```bash
python3 -m venv .venv
```

Windows

```bash
python -m venv .venv
```

Activate

Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install packages

```bash
pip install -r requirements.txt
```

Install Playwright browsers

```bash
playwright install
```

---

# 🔧 Environment Setup

Create

```
.env
```

Example

```env
N8N_JIRA_WEBHOOK_URL=http://localhost:5678/webhook/n8_project_name

CREATE_JIRA_TICKETS=true
```

---

# Figma Setup

Export

- PNG (Entire Frame)
- JSON using "Figma to JSON" Plugin

Place files

```
figma/
    expected/
        upload_modal.png

figma/
    figma_export.json
```

---

# Website Setup

Update

```
data/urls.py
```

Example

```python
BASE_URL = "https://your-vercel-app.vercel.app/"
```

---

#  Run

```bash
python test/main.py
```

---

#  Generated Reports

```
reports/

difference.png
highlighted.png

validation/

ai/

final/

jira/

report.html
```

---

# Workflow

```
Playwright Screenshot
        ↓
OpenCV Comparison
        ↓
Component Capture
        ↓
CSS Extraction
        ↓
DOM Extraction
        ↓
Layout Extraction
        ↓
Figma JSON Parsing
        ↓
Validation
        ↓
AI Analysis
        ↓
Final Report
        ↓
Jira Integration
        ↓
HTML Report
```

---

# Current Version

Version 1.0

Completed

- Visual Testing
- Component Validation
- CSS Validation
- AI Analysis
- HTML Dashboard
- Jira Automation

---

#  Planned Improvements

- Duplicate Jira Detection
- Responsive Testing
- Multiple Page Support
- PDF Reports
- GitHub Actions
- Jenkins Integration
- Framework Refactoring

---

# Author

**Sumudu Tharanga**

Associate QA Engineer

Built for learning, portfolio, and AI-powered software testing.