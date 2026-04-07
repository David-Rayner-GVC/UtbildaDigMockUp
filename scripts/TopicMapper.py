from pathlib import Path
import json


class TopicMapper:
    def __init__(self, mapping_file):
        self.mapping_path = Path(mapping_file)
        self._load_mappings()

    def _load_mappings(self):
        with open(self.mapping_path, "r", encoding="utf-8") as f:
            raw_mappings = json.load(f)

        # Build a lookup: normalized term → topic id
        self.term_to_id = {}

        for entry in raw_mappings:
            topic_id = entry["id"]
            for term in entry.get("terms", []):
                normalized = self._normalize(term)
                self.term_to_id[normalized] = topic_id

    def _normalize(self, text):
        """Normalize text for matching"""
        return text.strip().lower()

    def map(self, keywords):
        """Return list of matching topic ids (or None if no match)"""
        if not keywords:
            return None

        matched_ids = []

        for kw in keywords:
          norm_kw = self._normalize(kw)

          for term, topic_id in self.term_to_id.items():
            if term in norm_kw:
                if topic_id not in matched_ids:
                    matched_ids.append(topic_id)

        return matched_ids if matched_ids else None