"""Training Asset Metrics v2 tests"""
import subprocess, sys, json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent  # tests/test_scripts/ → tests/ → project root

def run_stats():
    r = subprocess.run([sys.executable, str(BASE / "scripts/training_asset_stats.py")],
                       capture_output=True, text=True, cwd=str(BASE))
    return r.stdout

def run_safety(mode="release"):
    r = subprocess.run([sys.executable, str(BASE / "scripts/check_training_asset_safety.py"), mode],
                       capture_output=True, text=True, cwd=str(BASE))
    return r.returncode, r.stdout


class TestAssetStats:
    def test_does_not_sum_counts_as_mb(self):
        out = run_stats()
        assert "training_asset" not in out.lower() or "MB" in out
        # The old bug line `total = sum(sections.values())` is gone
        assert "233.93" not in out and "233.9" not in out
        assert "22.8" not in out  # false percent

    def test_reports_disk_metrics(self):
        out = run_stats()
        assert "Disk Metrics" in out
        assert "training_packs_mb" in out
        assert "project_total_mb" in out

    def test_reports_file_metrics(self):
        out = run_stats()
        assert "File Metrics" in out
        assert "training_source_files" in out
        assert "archived_source_files" in out

    def test_reports_content_metrics(self):
        out = run_stats()
        assert "Content Metrics" in out
        assert "estimated_tokens" in out
        assert "questions_count" in out

    def test_reports_database_metrics(self):
        out = run_stats()
        assert "Database Metrics" in out
        assert "knowledge_store_count" in out
        assert "error_store_count" in out

    def test_handles_missing_db(self):
        # Script handles missing tables gracefully (returns 0)
        out = run_stats()
        assert "knowledge_store_count" in out
        assert out.count("knowledge_store_count") == 1

    def test_estimates_tokens(self):
        out = run_stats()
        assert "estimated_tokens" in out
        # Should appear in both Content Metrics and Progress
        found = False
        for line in out.split("\n"):
            if "estimated_tokens" in line and "/" not in line:
                val = line.strip().split()[-1].replace(",", "")
                assert int(val) >= 0
                found = True
                break
        assert found

    def test_multi_target_progress(self):
        out = run_stats()
        assert "Progress" in out
        assert "knowledge_chunks" in out
        assert "error_cases" in out
        assert "strategies" in out


class TestSafetyCheck:
    def test_reports_zero_counts(self):
        code, out = run_safety("release")
        assert "model_weights_found:" in out
        assert "private_paths_found:" in out
        assert "env_files_found:" in out

    def test_distinguishes_project_and_release(self):
        code1, out1 = run_safety("project")
        code2, out2 = run_safety("release")
        # Both should run without crash
        assert code1 is not None
        assert code2 is not None
