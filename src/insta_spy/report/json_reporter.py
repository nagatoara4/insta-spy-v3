"""
InstaSpy v3.0 — JSON Reporter
Generate professional JSON reports.
"""

import json
from datetime import datetime
from typing import Dict

class JSONReporter:
    """Generate professional JSON reports"""

    def __init__(self):
        self.version = "3.0.0"
        self.schema = "insta-spy-report-v3"

    def generate(self, data: Dict) -> str:
        """Generate JSON report"""
        report = {
            'metadata': {
                'tool': 'InstaSpy',
                'version': self.version,
                'schema': self.schema,
                'generated': datetime.now().isoformat()
            },
            'target': data.get('target', 'unknown'),
            'results': {
                'instagram': data.get('instagram'),
                'social_accounts': data.get('social_accounts', {}),
                'contacts': data.get('contacts'),
                'breaches': data.get('breaches', [])
            }
        }

        return json.dumps(report, indent=2, default=str)

    def save(self, data: Dict, filename: str) -> str:
        """Save report to file"""
        with open(filename, 'w') as f:
            f.write(self.generate(data))

        # Restrictive permissions
        import os
        os.chmod(filename, 0o600)

        return filename
