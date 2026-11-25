"""Deterministic classroom translation simulation; no microphone or live AI."""
from dataclasses import dataclass, asdict

@dataclass
class Result:
    original: str
    translation: str
    confidence: int
    needs_review: bool
    correction: str

EXAMPLES = {
    'climate': Result('Climate change can significantly affect marine ecosystems.', '气候变化可能会显著影响海洋生态系统。', 92, False, ''),
    'energy': Result('The study suggests that renewable energy could reduce the carbon footprint.', '这项研究表明，可再生能源可以减少碳足迹。', 58, True, '这项研究表明，可再生能源可能有助于减少碳足迹。'),
    'fifteen_high': Result('The lecturer says fifteen students joined the study.', '讲师说有五十名学生参加了研究。', 94, False, '讲师说有十五名学生参加了研究。'),
    'fifteen': Result('The lecturer says fifteen students joined the study.', '讲师说有五十名学生参加了研究。', 52, True, '讲师说有十五名学生参加了研究。'),
}

def simulate(example: str) -> dict:
    if example not in EXAMPLES:
        raise ValueError('Unknown example; select a supported scenario')
    return asdict(EXAMPLES[example])

def confirm_correction(example: str) -> dict:
    data = simulate(example)
    if not data['correction']:
        return data
    data['translation'] = data['correction']
    data['confidence'] = 95  # simulated confidence after review, not a measured probability
    data['needs_review'] = False
    data['correction'] = ''
    return data
