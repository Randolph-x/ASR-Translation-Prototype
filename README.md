# Lecture Translation — interactive prototype

Python 3.9+ and a browser. No dependencies or API keys.

```sh
python app.py
```

Open http://localhost:8001. Stop with Ctrl+C.

Choose a scenario and click **Start simulated listening**.

- Climate change: normal caption (92%).
- Renewable energy: ambiguous caption (58%); review the original and confirm the correction.
- Fifteen vs fifty: incorrect caption (52%); try confirming before viewing the original, then reveal it and confirm.
- Fifteen vs fifty (high-confidence error): compare the caption (50, 94%) with the simulated lecture slide (15), click **Flag possible error**, view the original, and confirm the suggested correction.

The fourth scenario extends the supplied Lab 3 prototype to demonstrate the Lab 2 high-confidence failure. The UI now clears stale captions when the scenario changes and disables controls during requests. The correction gate is client-side; the local API returns deterministic data. All captions and confidence scores are authored simulation data, including the 95% post-review value. No microphone, live ASR, translation model, recording, or retraining is implemented.

Run automated simulation tests:

```sh
python -m unittest discover -s tests -v
```

## Development record

| Stage | Design decision and evidence |
| --- | --- |
| Assignment 1 | Literature review, *Confidence Information and Error Correction in Automatic Speech Recognition*: confidence estimates can miss errors; extra markings may distract users. |
| Lab 2 | `01_lab2_worksheet.md`, `normal_storyboard.png`, `failure_recovery_storyboard.png`, and `flow.png`: visible confidence, selective warnings, review and recovery from high-confidence errors. |
| Lab 3 | `01_SPEC.md` and `02_PROMPT_LOG.md`: deadline test cases and a proposed number-validation step; the working simulation instead uses predefined study-participant captions. |
| Final prototype | Four scenarios (92%, 58%, 52%, 94%); manual flagging for the high-confidence error, a simulated lecture slide, original-text review, fixed suggested corrections, cleared stale captions and disabled controls during requests. Port 8001 distinguishes the retained version. |
| Validation | Nine Python unit tests passed. Four browser interaction paths were checked with simulated requests linked directly to the Python functions, including confirmation before and after revealing the original, and scenario reset. Full browser-to-HTTP integration was not verified in this check. |

Lab 4 is a separate course-question exercise and is not integrated into the translation prototype. Live audio, ASR, translation, number validation, audio replay, editable corrections, calibrated confidence and persistent feedback or retraining are not implemented.

## Submission record

- Public repository: https://github.com/Randolph-x/ASR-Translation-Prototype
- Public README: https://github.com/Randolph-x/ASR-Translation-Prototype/blob/main/README.md
- The submitted commit is identified in the project report.

## Use of AI and personal contribution

I used ChatGPT to help write and revise the Python, HTML, CSS and JavaScript code. I prepared the test cases and identified problems during development. I reviewed the proposed changes and selected the final four-scenario prototype based on my project scope.
