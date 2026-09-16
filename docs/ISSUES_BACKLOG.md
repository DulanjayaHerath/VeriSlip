# VeriSlip: 100 Engineering & Venture Issues Backlog

This backlog outlines **100 actionable, prioritized issues** divided across the 3 founder roles and shared engineering tracks for collaborative development on GitHub.

---

## 👥 Track & Ownership Summary

| Track | Primary Role | Issues Range | Focus Area |
| :--- | :--- | :--- | :--- |
| **Stream 1** | **Person 1: Forensic CV Lead** | Issues #1 – #28 | Layers 1–3: Bank Templates, ELA, DCT, Noise Residuals, Splicing |
| **Stream 2** | **Person 2: Data & ML Lead** | Issues #29 – #56 | Synthetic Generator, PII Redaction, Layer 4 Deep Learning Ensemble |
| **Stream 3** | **Person 3: Full-Stack & Biz Lead** | Issues #57 – #82 | FastAPI Server, Web Cockpit, WhatsApp Bot, Courier API, Monetization |
| **Stream 4** | **Shared Engineering & Research** | Issues #83 – #100 | CI/CD, Docker, Security/Ethics, Research Paper, Seller Pilot, Layer 5 |

---

## 🚀 How to Batch Import into GitHub

1. Authenticate GitHub CLI:
   ```bash
   gh auth login
   ```
2. Run the automated issue creator script:
   ```bash
   python3 scripts/create_github_issues.py --repo YOUR_GITHUB_USERNAME/VeriSlip
   ```
   *(Or preview first with `python3 scripts/create_github_issues.py --dry-run`)*

---

## 📋 Complete List of 100 Issues

### 🔬 Stream 1: Person 1 — Forensic Computer Vision (Issues #1 to #28)

#### #1: [PERSON1-CV] Implement ComBank Digital template layout grid and logo anchor verification
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:medium, layer:layer-1`

### Summary
Create exact pixel-grid anchor coordinates, logo aspect ratio, and header layout checks for Commercial Bank mobile banking receipts. Acceptance criteria: tests match genuine ComBank screenshots and detect mismatched header proportions.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #2: [PERSON1-CV] Implement Sampath Vishwa layout and color histogram matching
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:medium, layer:layer-1`

### Summary
Add template definitions for Sampath Vishwa app including orange branding palette (RGB 243, 112, 33) and field positions. Acceptance criteria: verifies Sampath slip layout fidelity.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #3: [PERSON1-CV] Implement Bank of Ceylon (BOC) Digi & SmartPay layout rules
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:medium, layer:layer-1`

### Summary
Define layout parameters for BOC Digi and SmartPay receipts. Acceptance criteria: validates header badge, gold color accents, and standard field offsets.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #4: [PERSON1-CV] Implement Hatton National Bank (HNB) SOLO & Digital Banking rules
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:medium, layer:layer-1`

### Summary
Add support for HNB digital banking receipts including reference regex and dark blue/gold branding validation.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #5: [PERSON1-CV] Add template matching for Seylan Bank (Seylan Mobile Banking)
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:medium, layer:layer-1`

### Summary
Implement template definition and field parser for Seylan Bank transfer receipts.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #6: [PERSON1-CV] Add template matching for Nations Trust Bank (NTB / FriMi)
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:medium, layer:layer-1`

### Summary
Support FriMi and Nations Trust Bank slip templates with signature magenta/blue accents.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #7: [PERSON1-CV] Add template matching for DFCC Bank and Pan Asia Bank
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:low, layer:layer-1`

### Summary
Add regex rules and color profiles for DFCC and Pan Asia Bank mobile receipts.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #8: [PERSON1-CV] Implement generic CEFTS & SLIPS interbank slip layout validator
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:low, layer:layer-1`

### Summary
Validate generic interbank transfer receipts complying with LankaPay CEFTS standard fields.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #9: [PERSON1-CV] Implement reference number checksum validation for Commercial Bank
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:medium, layer:layer-1`

### Summary
Research and implement reference number syntax and mod-checksum rules for ComBank transaction IDs.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #10: [PERSON1-CV] Implement reference number regex and length validator for Sampath & BOC
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:low, layer:layer-1`

### Summary
Validate reference number structures for Sampath Vishwa and BOC Digi, flagging synthetic sequential numbers.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #11: [PERSON1-CV] Build EXIF metadata parser with expanded editing software signatures
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:medium, layer:layer-1`

### Summary
Expand KNOWN_EDITING_SOFTWARE list to include Pixelmator, Photopea, VSCO, InShot, Procreate, and detect stripped EXIF markers.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #12: [PERSON1-CV] Add PNG chunk metadata inspection for software and author signatures
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:low, layer:layer-1`

### Summary
Parse PNG textual chunks (tEXt, zTXt, iTXt) to identify software signatures injected by web/desktop image editors.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #13: [PERSON1-CV] Implement timestamp sanity checks against displayed slip dates
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:medium, layer:layer-1`

### Summary
Cross-reference file creation/modification timestamps with receipt displayed date/time to flag retroactively altered slips.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #14: [PERSON1-CV] Mobile screenshot aspect ratio and DPI resolution classifier
* **Role:** `person1-cv` | **Layer:** `Layer 1` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `role:person1-cv, milestone:phase-1, priority:low, layer:layer-1`

### Summary
Detect non-standard smartphone resolutions, upscaling artifacts, and desktop browser inspect-element proportions.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #15: [PERSON1-CV] Implement multi-scale Error Level Analysis (ELA) with adaptive quality factors
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:high, layer:layer-2`

### Summary
Evaluate image across multiple JPEG compression quality factors (Q75, Q85, Q90, Q95) and select optimal scale based on image base quality.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #16: [PERSON1-CV] Implement chromatic vs luminance ELA difference decomposition
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:high, layer:layer-2`

### Summary
Decompose ELA analysis into Y (luminance) and CbCr (chrominance) channels. Spliced text often exhibits anomalies predominantly in luminance.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #17: [PERSON1-CV] Build 8x8 block-wise 2D-DCT AC frequency coefficient histogram analyzer
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:high, layer:layer-2`

### Summary
Extract DCT coefficients for primary AC frequencies (1,2) and (2,1) across 8x8 blocks to calculate periodicity index.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #18: [PERSON1-CV] Implement double-JPEG compression grid alignment and shift detector
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:high, layer:layer-2`

### Summary
Detect non-aligned 8x8 JPEG block grids which occur when a cropped slip or spliced element is saved with different block boundaries.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #19: [PERSON1-CV] Implement copy-move forgery detection using ORB/SIFT keypoint matching
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person1-cv, milestone:phase-3, priority:high, layer:layer-2`

### Summary
Detect cloned digits or pasted bank logos by clustering matched feature points between distinct regions of the receipt.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #20: [PERSON1-CV] Implement block-based DCT correlation for dense copy-move detection
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person1-cv, milestone:phase-3, priority:high, layer:layer-2`

### Summary
Divide image into overlapping blocks and compute lexicographic sorting of DCT coefficients to identify duplicated image patches.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #21: [PERSON1-CV] Build font stroke-width and edge anti-aliasing consistency checker
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:medium, layer:layer-2`

### Summary
Measure Laplacian edge energy and gradient profile across text characters to detect font sharpness disparities between amount and card labels.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #22: [PERSON1-CV] Implement text baseline alignment and spacing disparity detector
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:medium, layer:layer-2`

### Summary
Detect vertical jitter, misaligned baseline bounding boxes, and uneven kerning introduced by manual text insertion.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #23: [PERSON1-CV] Implement Spatial Rich Models (SRM) high-pass filtering kernels
* **Role:** `person1-cv` | **Layer:** `Layer 3` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person1-cv, milestone:phase-3, priority:high, layer:layer-3`

### Summary
Apply standard 3x3 and 5x5 SRM linear and non-linear filter kernels to extract subtle noise residuals from screenshot canvas.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #24: [PERSON1-CV] Calibrate noise residual variance estimation for flat UI backgrounds
* **Role:** `person1-cv` | **Layer:** `Layer 3` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:medium, layer:layer-3`

### Summary
Ensure edge-masked background regions calculate baseline noise variance without interference from typography anti-aliasing.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #25: [PERSON1-CV] Implement local noise variance discontinuity clustering
* **Role:** `person1-cv` | **Layer:** `Layer 3` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:medium, layer:layer-3`

### Summary
Cluster neighboring outlier blocks to form coherent bounding boxes around erased or clone-stamped patches.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #26: [PERSON1-CV] Detect median filter smoothing traces from brush / blur tools
* **Role:** `person1-cv` | **Layer:** `Layer 3` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person1-cv, milestone:phase-3, priority:high, layer:layer-3`

### Summary
Analyze residual difference histograms to detect when an attacker applied a blur tool to blend forged numbers into the receipt.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #27: [PERSON1-CV] Build visual side-by-side forensic heatmap generator (Jet/Inferno/Viridis)
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person1-cv, milestone:phase-2, priority:low, layer:layer-2`

### Summary
Generate publication-ready composite images showing original slip side-by-side with ELA heatmap and noise residual map.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #28: [PERSON1-CV] Optimize OpenCV forensic feature extraction pipeline for <500ms latency
* **Role:** `person1-cv` | **Layer:** `Layer 2` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `role:person1-cv, milestone:phase-3, priority:medium, layer:layer-2`

### Summary
Vectorize numpy loops and optimize image downsamping for high-throughput API execution.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.



---

### 🧠 Stream 2: Person 2 — Data Engineering & Deep Learning (Issues #29 to #56)

#### #29: [PERSON2-ML] Expand Synthetic Slip Generator to support all 5 top Sri Lankan bank templates
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-1, priority:medium, layer:synthetic-data`

### Summary
Add high-fidelity vector rendering for ComBank, Sampath Vishwa, BOC Digi, HNB SOLO, and CEFTS slips.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #30: [PERSON2-ML] Implement multi-tier tampering attack: Novice skill level
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-1, priority:medium, layer:synthetic-data`

### Summary
Simulate novice edits: obvious font mismatches, misaligned text, uncompressed PNG text pasted on compressed JPEG.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #31: [PERSON2-ML] Implement multi-tier tampering attack: Intermediate skill level
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-2, priority:medium, layer:synthetic-data`

### Summary
Simulate intermediate edits: matched font family, approximate color match, and single recompression step.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #32: [PERSON2-ML] Implement multi-tier tampering attack: Expert / Skilled level
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:high, layer:synthetic-data`

### Summary
Simulate skilled adversary: matched font weight, anti-aliasing smoothing, matching local noise floor, and double-JPEG alignment.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #33: [PERSON2-ML] Implement synthetic amount manipulation attack module
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `role:person2-ml, milestone:phase-1, priority:low, layer:synthetic-data`

### Summary
Simulate replacing transaction amounts with 10x or 100x inflated values while generating exact ground-truth bounding boxes.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #34: [PERSON2-ML] Implement synthetic reference number tampering module
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `role:person2-ml, milestone:phase-1, priority:low, layer:synthetic-data`

### Summary
Simulate forged reference numbers with spliced digits or altered prefixes.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #35: [PERSON2-ML] Implement synthetic beneficiary name & account swapping module
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person2-ml, milestone:phase-2, priority:low, layer:synthetic-data`

### Summary
Simulate swapping beneficiary names and masked account numbers on receipts.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #36: [PERSON2-ML] Implement date/timestamp modification attack module
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person2-ml, milestone:phase-2, priority:low, layer:synthetic-data`

### Summary
Simulate recycling old payment slips by doctoring the transaction timestamp and date.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #37: [PERSON2-ML] Build COCO & Pascal VOC annotation exporter for synthetic dataset
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-2, priority:medium, layer:synthetic-data`

### Summary
Export generated tampered receipts with standard COCO JSON format bounding boxes and segmentation masks for object detection models.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #38: [PERSON2-ML] Implement automated dataset generation CLI script with configurable sample count
* **Role:** `person2-ml` | **Layer:** `Synthetic Data` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person2-ml, milestone:phase-2, priority:low, layer:synthetic-data`

### Summary
Create script  with balanced authentic and tampered distributions.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #39: [PERSON2-ML] Build automated PII redaction pipeline for collected real receipts
* **Role:** `person2-ml` | **Layer:** `Dataset` | **Milestone:** `Phase 1: Foundations` | **Priority:** `High`
* **Labels:** `role:person2-ml, milestone:phase-1, priority:high, layer:dataset`

### Summary
Automatically detect, blur, or synthesize real customer names, account numbers, and phone numbers before storing in research datasets.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #40: [PERSON2-ML] Collect and curate initial benchmark set of 200 permission-cleared genuine slips
* **Role:** `person2-ml` | **Layer:** `Dataset` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-2, priority:medium, layer:dataset`

### Summary
Gather consent-cleared slips from team transactions and merchant friends across different mobile operating systems (iOS and Android).

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #41: [PERSON2-ML] Create stratified dataset train/validation/test splits by bank and skill tier
* **Role:** `person2-ml` | **Layer:** `Dataset` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-2, priority:medium, layer:dataset`

### Summary
Establish strict train/val/test splits ensuring no bank template leakage to test zero-shot generalization on unseen bank templates.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #42: [PERSON2-ML] Create adversarial benchmark test set with human-edited slips (Photoshop/Canva)
* **Role:** `person2-ml` | **Layer:** `Dataset` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:high, layer:dataset`

### Summary
Manually tamper 50 genuine slips using real photo editing software to create a golden evaluation benchmark.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #43: [PERSON2-ML] Implement dataset integrity and checksum verification script
* **Role:** `person2-ml` | **Layer:** `Dataset` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person2-ml, milestone:phase-2, priority:low, layer:dataset`

### Summary
Verify SHA-256 hashes and image validity for all dataset samples to prevent corrupt training samples.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #44: [PERSON2-ML] Create dataset documentation and data card following ethical research standards
* **Role:** `person2-ml` | **Layer:** `Dataset` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Low`
* **Labels:** `role:person2-ml, milestone:phase-4, priority:low, layer:dataset`

### Summary
Document dataset provenance, redaction methodology, distribution statistics, and dual-use ethical safeguards.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #45: [PERSON2-ML] Design PyTorch dual-stream fusion model architecture (RGB + Forensic Maps)
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:high, layer:layer-4`

### Summary
Build a PyTorch model accepting 3-channel RGB image alongside 3-channel forensic tensor (ELA + Noise + DCT).

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #46: [PERSON2-ML] Implement EfficientNet-B0 backbone feature extractor for RGB stream
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:medium, layer:layer-4`

### Summary
Use pretrained EfficientNet-B0 or ConvNeXt-Tiny to extract 512-dim visual representation from receipt patches.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #47: [PERSON2-ML] Implement CNN feature extractor for multi-channel forensic map stream
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:medium, layer:layer-4`

### Summary
Build a lightweight 4-layer convolutional network extracting high-frequency tampering signatures from forensic maps.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #48: [PERSON2-ML] Implement cross-attention fusion layer combining visual and forensic features
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:high, layer:layer-4`

### Summary
Fuse RGB features with forensic features using cross-attention or gated feature fusion before classification head.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #49: [PERSON2-ML] Implement binary classification head with temperature calibration
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:medium, layer:layer-4`

### Summary
Train classification head with Platt scaling / temperature scaling to output true calibrated tamper probabilities.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #50: [PERSON2-ML] Implement U-Net / FPN segmentation head for pixel-level tamper localization
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:high, layer:layer-4`

### Summary
Add segmentation decoder predicting binary tampering mask highlighting exact forged regions.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #51: [PERSON2-ML] Implement combined loss function: Focal Loss + Dice Loss for class imbalance
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:medium, layer:layer-4`

### Summary
Handle sparse tampered pixels using combined Focal and Dice loss formulation.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #52: [PERSON2-ML] Build PyTorch training and validation pipeline with TensorBoard logging
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-3, priority:medium, layer:layer-4`

### Summary
Write training loop with learning rate scheduling, early stopping, and metric logging.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #53: [PERSON2-ML] Evaluate Layer 4 model performance across skill tiers (Novice, Intermediate, Expert)
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-4, priority:medium, layer:layer-4`

### Summary
Generate evaluation tables reporting Precision, Recall, F1, and ROC-AUC per difficulty tier.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #54: [PERSON2-ML] Conduct ablation study: Classical layers vs Deep Learning vs Fusion Ensemble
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `High`
* **Labels:** `role:person2-ml, milestone:phase-4, priority:high, layer:layer-4`

### Summary
Demonstrate that the ensemble outperforms any single classical or learned detector in isolation.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #55: [PERSON2-ML] Quantize PyTorch model to INT8 / ONNX format for rapid CPU inference
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-4, priority:medium, layer:layer-4`

### Summary
Export model to ONNX runtime with INT8 dynamic quantization for <100ms inference without GPU.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #56: [PERSON2-ML] Package Layer 4 inference module into unified engine pipeline
* **Role:** `person2-ml` | **Layer:** `Layer 4` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `role:person2-ml, milestone:phase-4, priority:medium, layer:layer-4`

### Summary
Integrate trained model checkpoint into  and connect with .

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.



---

### 🌐 Stream 3: Person 3 — Backend, Product & Monetization (Issues #57 to #82)

#### #57: [PERSON3-FULLSTACK] Implement API Key authentication and multi-tier rate limiting
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:medium, layer:backend-api`

### Summary
Add API key middleware with Redis or in-memory token bucket limiting free tier to 10 requests/day and pro tier to 100/min.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #58: [PERSON3-FULLSTACK] Implement asynchronous background task processing for heavy forensic scans
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:medium, layer:backend-api`

### Summary
Use FastAPI background tasks or Celery/RQ for processing high-resolution slips without blocking event loop.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #59: [PERSON3-FULLSTACK] Add structured JSON logging with request tracing and correlation IDs
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:low, layer:backend-api`

### Summary
Implement structured logging with correlation IDs for tracing verification requests across layers.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #60: [PERSON3-FULLSTACK] Implement merchant telemetry and fraud analytics aggregation endpoints
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:backend-api`

### Summary
Add  returning daily scan volume, fraud detection rate, and common tampered bank templates.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #61: [PERSON3-FULLSTACK] Implement webhook notification dispatcher for asynchronous order verification
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:backend-api`

### Summary
Enable merchants to register webhook URLs to receive verification callbacks when scans complete.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #62: [PERSON3-FULLSTACK] Add image sanitization and virus/bomb prevention middleware
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:medium, layer:backend-api`

### Summary
Validate image file headers, maximum dimensions, decompression bomb thresholds, and strip malicious payloads.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #63: [PERSON3-FULLSTACK] Implement OpenAPI / Swagger documentation enhancements and interactive examples
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:low, layer:backend-api`

### Summary
Provide rich example payloads and detailed field descriptions on  and .

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #64: [PERSON3-FULLSTACK] Implement CORS policies and production security headers
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:low, layer:backend-api`

### Summary
Configure secure CORS origins, HSTS, X-Content-Type-Options, and Content-Security-Policy headers.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #65: [PERSON3-FULLSTACK] Add health check probe with detailed component readiness diagnostics
* **Role:** `person3-fullstack` | **Layer:** `Backend API` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-1, priority:low, layer:backend-api`

### Summary
Enhance  endpoint to verify model weights loaded, memory status, and disk availability.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #66: [PERSON3-FULLSTACK] Implement Meta WhatsApp Cloud API webhook receiver and signature verification
* **Role:** `person3-fullstack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `High`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:high, layer:whatsapp-bot`

### Summary
Build production endpoint for Meta WhatsApp Business Cloud API with HMAC SHA-256 signature verification.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #67: [PERSON3-FULLSTACK] Implement WhatsApp media downloader and temporary image buffer
* **Role:** `person3-fullstack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:whatsapp-bot`

### Summary
Download customer media attachments from WhatsApp media endpoints securely into memory.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #68: [PERSON3-FULLSTACK] Implement WhatsApp conversational state machine and onboarding message flow
* **Role:** `person3-fullstack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:whatsapp-bot`

### Summary
Handle seller onboarding, balance check commands (balance), and help menus in English and Sinhala/Tamil.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #69: [PERSON3-FULLSTACK] Build automated WhatsApp image annotation returning red-boxed tamper slips
* **Role:** `person3-fullstack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:whatsapp-bot`

### Summary
When fraud is detected, draw red bounding boxes on the slip image and send it back to the seller via WhatsApp media message.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #70: [PERSON3-FULLSTACK] Implement merchant subscription credit balance tracker for WhatsApp bot
* **Role:** `person3-fullstack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:whatsapp-bot`

### Summary
Track checks used per phone number, notifying user when free quota is reached with payment upgrade link.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #71: [PERSON3-FULLSTACK] Add mock WhatsApp interactive test dashboard for local developer testing
* **Role:** `person3-fullstack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:low, layer:whatsapp-bot`

### Summary
Refine Web Cockpit WhatsApp simulator tab to allow testing custom phone numbers and arbitrary image uploads.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #72: [PERSON3-FULLSTACK] Integrate Sri Lankan SMS fallback notification via Dialog/Mobitel SMS gateway
* **Role:** `person3-fullstack` | **Layer:** `WhatsApp Bot` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-4, priority:low, layer:whatsapp-bot`

### Summary
Send SMS alert to seller if a high-risk fraud attempt occurs while seller is offline.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #73: [PERSON3-FULLSTACK] Implement interactive zoom and pan controls on inspection canvas
* **Role:** `person3-fullstack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:low, layer:web-frontend`

### Summary
Allow users to zoom in up to 400% on highlighted tamper bounding boxes to inspect subpixel artifacts.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #74: [PERSON3-FULLSTACK] Add side-by-side split screen view comparing original slip and ELA heatmap
* **Role:** `person3-fullstack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:medium, layer:web-frontend`

### Summary
Add slider handle to swipe between raw screenshot and forensic heatmap view.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #75: [PERSON3-FULLSTACK] Build merchant history drawer with past verification search and filter
* **Role:** `person3-fullstack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:web-frontend`

### Summary
Allow merchants to view previously checked slips with search by reference number or date.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #76: [PERSON3-FULLSTACK] Add light/dark theme toggle and mobile-responsive viewport tuning
* **Role:** `person3-fullstack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-2, priority:low, layer:web-frontend`

### Summary
Optimize CSS for mobile browser viewing on seller smartphones.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #77: [PERSON3-FULLSTACK] Implement keyboard shortcuts for rapid merchant triage (Space: Accept, X: Flag)
* **Role:** `person3-fullstack` | **Layer:** `Web Frontend` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Low`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:low, layer:web-frontend`

### Summary
Power-seller shortcuts for high-speed review of multiple slips during peak sales.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #78: [PERSON3-FULLSTACK] Implement dedicated Courier Rider API endpoint 
* **Role:** `person3-fullstack` | **Layer:** `Courier B2B` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:courier-b2b`

### Summary
Streamlined response payload optimized for mobile courier apps with simple boolean .

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #79: [PERSON3-FULLSTACK] Build WooCommerce plugin boilerplate for direct bank transfer auto-verification
* **Role:** `person3-fullstack` | **Layer:** `E-Commerce` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `High`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:high, layer:e-commerce`

### Summary
Create WordPress/WooCommerce plugin that intercepts order checkout receipt uploads and queries VeriSlip API.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #80: [PERSON3-FULLSTACK] Build Shopify Webhook app integration for manual payment screening
* **Role:** `person3-fullstack` | **Layer:** `E-Commerce` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `High`
* **Labels:** `role:person3-fullstack, milestone:phase-4, priority:high, layer:e-commerce`

### Summary
Develop Shopify app listening to order creation events and screening attached wire deposit proofs.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #81: [PERSON3-FULLSTACK] Implement formal PDF Forensic Audit Report generator with cryptographic seal
* **Role:** `person3-fullstack` | **Layer:** `Audit Report` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:medium, layer:audit-report`

### Summary
Generate publication-grade PDF report with timestamp, SHA-256 hash, ELA diagrams, and legal evidence format.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #82: [PERSON3-FULLSTACK] Implement payment gateway integration (PayHere / Stripe / Genie) for Pro subscriptions
* **Role:** `person3-fullstack` | **Layer:** `Monetization` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `High`
* **Labels:** `role:person3-fullstack, milestone:phase-3, priority:high, layer:monetization`

### Summary
Integrate local Sri Lankan payment gateways for charging LKR 1,490/mo Pro subscriptions and credit top-ups.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.



---

### ⚙️ Stream 4: Shared Systems, DevOps, Research Paper & Pilot (Issues #83 to #100)

#### #83: [SHARED] Setup GitHub Actions CI pipeline running pytest and code coverage
* **Role:** `shared` | **Layer:** `DevOps` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-1, priority:medium, layer:devops`

### Summary
Automate unit tests on every pull request with pytest, codecov, and linting checks.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #84: [SHARED] Setup Flake8, Black, and isort pre-commit hooks
* **Role:** `shared` | **Layer:** `DevOps` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Low`
* **Labels:** `role:shared, milestone:phase-1, priority:low, layer:devops`

### Summary
Maintain code style and automated formatting across all team contributions.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #85: [SHARED] Create multi-stage Dockerfile for FastAPI backend and frontend static assets
* **Role:** `shared` | **Layer:** `DevOps` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-2, priority:medium, layer:devops`

### Summary
Build lightweight production Docker container (<400MB) with non-root user.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #86: [SHARED] Create Docker Compose configuration with Redis and Nginx reverse proxy
* **Role:** `shared` | **Layer:** `DevOps` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-2, priority:medium, layer:devops`

### Summary
Provide single-command local development and production orchestration ().

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #87: [SHARED] Configure deployment pipeline to cloud host (Render / Railway / AWS EC2)
* **Role:** `shared` | **Layer:** `DevOps` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-3, priority:medium, layer:devops`

### Summary
Deploy staging environment for live team and merchant beta testing.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #88: [SHARED] Setup Prometheus metrics and Grafana dashboard for API latency monitoring
* **Role:** `shared` | **Layer:** `DevOps` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Low`
* **Labels:** `role:shared, milestone:phase-4, priority:low, layer:devops`

### Summary
Monitor request latency, layer execution times, and memory utilization.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #89: [SHARED] Implement dual-use containment: lock down synthetic tampering generator
* **Role:** `shared` | **Layer:** `Security` | **Milestone:** `Phase 1: Foundations` | **Priority:** `High`
* **Labels:** `role:shared, milestone:phase-1, priority:high, layer:security`

### Summary
Ensure synthetic tampering code is strictly internal, isolated from public API endpoints, and protected by environment flags.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #90: [SHARED] Implement automated PII scrubbing on all request logs and stored samples
* **Role:** `shared` | **Layer:** `Security` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `High`
* **Labels:** `role:shared, milestone:phase-2, priority:high, layer:security`

### Summary
Hash bank account numbers and redact personal names before persisting any audit records.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #91: [SHARED] Implement rate-limiting and IP reputation against adversarial probing
* **Role:** `shared` | **Layer:** `Security` | **Milestone:** `Phase 3: Product & Integrations` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-3, priority:medium, layer:security`

### Summary
Prevent fraudsters from querying the API repeatedly to reverse-engineer evasion techniques.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #92: [SHARED] Perform security review on file upload handling and path traversal vulnerabilities
* **Role:** `shared` | **Layer:** `Security` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-2, priority:medium, layer:security`

### Summary
Audit file uploads against SVG script injection, path traversal, and decompression attacks.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #93: [SHARED] Conduct literature review on financial document forgery vs natural image forensics
* **Role:** `shared` | **Layer:** `Research Paper` | **Milestone:** `Phase 1: Foundations` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-1, priority:medium, layer:research-paper`

### Summary
Compile comprehensive bibliography and related work section covering ELA, copy-move, and document verification.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #94: [SHARED] Draft Research Paper: Problem Formulation & Threat Model section
* **Role:** `shared` | **Layer:** `Research Paper` | **Milestone:** `Phase 2: Core Forensics` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-2, priority:medium, layer:research-paper`

### Summary
Formulate mathematical threat model characterizing the Sri Lankan P2P payment fraud ecosystem.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #95: [SHARED] Draft Research Paper: Multi-Layer Architecture & Methodology section
* **Role:** `shared` | **Layer:** `Research Paper` | **Milestone:** `Phase 3: ML & Advanced Forensics` | **Priority:** `High`
* **Labels:** `role:shared, milestone:phase-3, priority:high, layer:research-paper`

### Summary
Document mathematical formulations for Layer 1, Layer 2 (ELA/DCT), Layer 3 (Noise), and Layer 4 (Ensemble).

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #96: [SHARED] Generate experimental results tables, ROC curves, and confusion matrices
* **Role:** `shared` | **Layer:** `Research Paper` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `High`
* **Labels:** `role:shared, milestone:phase-4, priority:high, layer:research-paper`

### Summary
Produce publication figures comparing single layers against the ensemble across skill tiers.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #97: [SHARED] Finalize conference submission draft for IEEE MERCon / ICTer
* **Role:** `shared` | **Layer:** `Research Paper` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `High`
* **Labels:** `role:shared, milestone:phase-4, priority:high, layer:research-paper`

### Summary
Format paper into IEEE two-column template, polish figures, and complete peer-review readiness check.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #98: [SHARED] Run 2-week closed beta pilot with 10 Sri Lankan social media sellers
* **Role:** `shared` | **Layer:** `GTM & Pilot` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-4, priority:medium, layer:gtm-&-pilot`

### Summary
Distribute WhatsApp bot to friendly Instagram/FB Marketplace sellers; collect user feedback and false positive logs.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #99: [SHARED] Draft B2B proposal and pilot deck for Sri Lankan courier logistics operators
* **Role:** `shared` | **Layer:** `GTM & Pilot` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Low`
* **Labels:** `role:shared, milestone:phase-4, priority:low, layer:gtm-&-pilot`

### Summary
Create presentation deck highlighting COD rider fraud prevention ROI for Domex, PromptX, and Koombiyo.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.


#### #100: [SHARED] Formulate technical roadmap for Layer 5: LankaPay / CEFTS API Direct Verification Gateway
* **Role:** `shared` | **Layer:** `GTM & Pilot` | **Milestone:** `Phase 4: Research & GTM` | **Priority:** `Medium`
* **Labels:** `role:shared, milestone:phase-4, priority:medium, layer:gtm-&-pilot`

### Summary
Document architectural transition from image forensics to an authorized programmatic transaction verification gateway with local banks.

### Track & Ownership
* **Primary Role:** 
* **Forensic Layer:** 
* **Milestone:** 
* **Priority / Complexity:** 

### Acceptance Criteria
- [ ] Requirements specified in description implemented.
- [ ] Unit tests added covering functionality.
- [ ] No regression on existing test suite (============================= test session starts ==============================
platform darwin -- Python 3.10.11, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/chirana/IdeaProjects/VeriSlip
plugins: dash-3.3.0, timeout-2.4.0, anyio-3.7.1, langsmith-0.7.22
collected 0 items / 4 errors

==================================== ERRORS ====================================
______________________ ERROR collecting tests/test_api.py ______________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_api.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_api.py:6: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
___________________ ERROR collecting tests/test_generator.py ___________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_generator.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_generator.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
____________________ ERROR collecting tests/test_layer1.py _____________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer1.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer1.py:6: in <module>
    from core.templates.bank_rules import validate_reference_number, identify_bank_from_text
E   ModuleNotFoundError: No module named 'core'
_________________ ERROR collecting tests/test_layer2_layer3.py _________________
ImportError while importing test module '/Users/chirana/IdeaProjects/VeriSlip/tests/test_layer2_layer3.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
tests/test_layer2_layer3.py:5: in <module>
    from core.ml.dataset_generator import SyntheticSlipGenerator
E   ModuleNotFoundError: No module named 'core'
=========================== short test summary info ============================
ERROR tests/test_api.py
ERROR tests/test_generator.py
ERROR tests/test_layer1.py
ERROR tests/test_layer2_layer3.py
!!!!!!!!!!!!!!!!!!! Interrupted: 4 errors during collection !!!!!!!!!!!!!!!!!!!!
============================== 4 errors in 0.19s ===============================).
- [ ] Documentation or inline docstrings updated.

