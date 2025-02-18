import pytest

from credsweeper.filters import ValueArrayDictionaryCheck, VariableNotAllowedPatternCheck
from credsweeper.rules import Rule
from tests.filters.conftest import LINE_VALUE_PATTERN, DUMMY_ANALYSIS_TARGET
from tests.test_utils.dummy_line_data import get_line_data


class TestValueArrayDictionaryCheck:

    @pytest.fixture
    def token_rule(self, config) -> Rule:
        token_rule_without_filters = {
            "name": "Token",
            "severity": "medium",
            "type": "keyword",
            "values": ["token"],
            "filter_type": [VariableNotAllowedPatternCheck.__name__],
            "use_ml": True,
            "min_line_len": 0,
            "validations": [],
            "doc_available": True,
        }
        rule = Rule(config, token_rule_without_filters)
        return rule

    def test_value_array_dictionary_p(self, file_path: pytest.fixture, success_line: pytest.fixture) -> None:
        line_data = get_line_data(file_path, line=success_line, pattern=LINE_VALUE_PATTERN)
        assert ValueArrayDictionaryCheck().run(line_data, DUMMY_ANALYSIS_TARGET) is False

    @pytest.mark.parametrize("line", ["token = values[i]", "token = values[token_id]", "token = values[k+1 : j]"])
    def test_value_array_dictionary_n(self, token_rule: Rule, file_path: pytest.fixture, line: str) -> None:
        """Evaluate that filter do remove calls to arrays and arrays declarations"""
        line_data = get_line_data(file_path, line=line, pattern=token_rule.patterns[0])
        assert ValueArrayDictionaryCheck().run(line_data, DUMMY_ANALYSIS_TARGET) is True

    @pytest.mark.parametrize("line", [
        "token[i] = 'root'", "users[i] = {token: 'root'}", "user = {token: 'root'}", "token = {'root'}",
        "user = get_user_data(token='root', user=users[i])", "user = get_user_data(user=users[i], token='root')"
    ])
    def test_array_assignment_p(self, token_rule: Rule, file_path: pytest.fixture, line: str) -> None:
        """Evaluate that filter do not remove assignments to array or dictionary declaration"""
        line_data = get_line_data(file_path, line=line, pattern=token_rule.patterns[0])
        assert ValueArrayDictionaryCheck().run(line_data, DUMMY_ANALYSIS_TARGET) is False

    def test_value_array_dictionary_none_value_n(self, file_path: pytest.fixture, success_line: pytest.fixture) -> None:
        line_data = get_line_data(file_path, line=success_line)
        assert ValueArrayDictionaryCheck().run(line_data, DUMMY_ANALYSIS_TARGET) is True
