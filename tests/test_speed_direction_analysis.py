from pathlib import Path

import polars as pl
import pytest

from beehaviourlab.tracking import speed_direction_analysis as sda


def test_global_analysis_writes_outputs(tmp_path: Path) -> None:
    df = pl.read_csv("tests/data/sample_vid_yolo_tracking_fixed_ids_velocity.csv")
    sda.global_analysis(df, tmp_path, "sample")

    expected = [
        "sample_glob_speed_stats.csv",
        "sample_glob_speed_hist.png",
        "sample_obj_speed_stats.csv",
        "sample_per_obj_speed_hist.png",
        "sample_glob_dir_hist.png",
        "sample_per_obj_dir_hist.png",
    ]
    for name in expected:
        assert (tmp_path / name).exists()

    stats = pl.read_csv(tmp_path / "sample_glob_speed_stats.csv")
    assert "statistic" in stats.columns
    assert stats["value"].max() > 0


def test_main_generates_outputs(tmp_path: Path) -> None:
    input_csv = Path("tests/data/sample_vid_yolo_tracking_fixed_ids_velocity.csv")
    result = sda.main.callback(input_csv, tmp_path)

    assert result is None
    assert (tmp_path / f"{input_csv.stem}_glob_speed_stats.csv").exists()


def test_main_errors_on_missing_columns(tmp_path: Path) -> None:
    df = pl.DataFrame({"stable_id": [1], "speed": [1.0]})
    csv_path = tmp_path / "missing.csv"
    df.write_csv(csv_path)

    with pytest.raises(Exception) as exc:
        sda.main.callback(csv_path, tmp_path)

    assert "Missing columns" in str(exc.value)


def test_main_errors_on_no_speed(tmp_path: Path) -> None:
    df = pl.DataFrame(
        {"stable_id": [1], "speed": [None], "dx": [0.0], "dy": [0.0]}
    )
    csv_path = tmp_path / "empty.csv"
    df.write_csv(csv_path)

    with pytest.raises(Exception) as exc:
        sda.main.callback(csv_path, tmp_path)

    assert "No valid speed data found" in str(exc.value)


def test_main_errors_on_empty_input(tmp_path: Path) -> None:
    df = pl.DataFrame(
        {
            "stable_id": pl.Series([], dtype=pl.Int64),
            "speed": pl.Series([], dtype=pl.Float64),
            "dx": pl.Series([], dtype=pl.Float64),
            "dy": pl.Series([], dtype=pl.Float64),
        }
    )
    csv_path = tmp_path / "empty.csv"
    df.write_csv(csv_path)

    with pytest.raises(Exception) as exc:
        sda.main.callback(csv_path, tmp_path)

    assert "No valid speed data found" in str(exc.value)
