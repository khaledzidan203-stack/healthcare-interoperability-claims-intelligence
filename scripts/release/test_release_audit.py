"""In-memory negative checks for release boundary and scanner regressions."""
import unittest

from release_audit import ASSIGNMENT, LOCAL_PATH, PRIVATE_PROBES, ROOT, SECRET, git_ignored_paths, ignore_rules, ignored


class ReleaseBoundaryTests(unittest.TestCase):
    def test_private_paths_are_excluded(self):
        rules = ignore_rules(ROOT)
        for path in PRIVATE_PROBES:
            with self.subTest(path=path):
                self.assertTrue(ignored(path, rules))
        if (ROOT / '.git').exists():
            self.assertEqual(git_ignored_paths(ROOT, PRIVATE_PROBES), set(PRIVATE_PROBES))

    def test_credential_rule_removal_is_detectable(self):
        rules = [r for r in ignore_rules(ROOT) if r != '.env']
        self.assertFalse(ignored('.env', rules))

    def test_public_exceptions_survive(self):
        for path in ('.env.example', 'data/raw/.gitkeep', 'logs/.gitkeep'):
            self.assertFalse(ignored(path, ignore_rules(ROOT)))

    def test_nested_powerbi_cache(self):
        rules = ignore_rules(ROOT)
        for path in ('powerbi/.pbi/local.json', 'powerbi/a/b/.pbi/local.json'):
            self.assertTrue(ignored(path, rules))
        self.assertFalse(ignored('powerbi/a/definition.pbir', rules))

    def test_token_signature_detection(self):
        self.assertIsNotNone(SECRET.search('ghp_' + 'a' * 36))
        self.assertIsNone(SECRET.search('ordinary schema field access_token'))

    def test_multiline_credential_literal(self):
        sample = 'client_' + 'secret' + ' =\n"' + 'invented-value' + '"'
        self.assertIsNotNone(ASSIGNMENT.search(sample))
        self.assertIsNone(ASSIGNMENT.search('client_' + 'secret = settings.value'))

    def test_urls_not_confused_with_drive_paths(self):
        self.assertIsNone(LOCAL_PATH.search('https://example.org/schema.json'))
        self.assertIsNotNone(LOCAL_PATH.search('Z' + ':' + '/' + 'private/file'))


if __name__ == '__main__':
    unittest.main()
