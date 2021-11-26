from pathlib import Path

from credsweeper.file_handler.text_content_provider import TextContentProvider

class TestTextContentProvider:
    def test_get_analysis_target_p(self) -> None:
        """Evaluate that lines data correctly extracted from file"""
        file_path = Path(__file__).resolve().parent.parent
        target_path = file_path/"samples"/"password"
        content_provider = TextContentProvider(target_path)

        analysis_targets = content_provider.get_analysis_target()

        all_lines = ['password = "cackle!"', '']

        assert len(analysis_targets) == 2

        target = analysis_targets[0]
        assert target.line == 'password = "cackle!"'
        assert target.line_num == 1
        assert target.lines == all_lines
        assert target.file_path == target_path
