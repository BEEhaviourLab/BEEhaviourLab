from pathlib import Path

import polars as pl
import pytest

from beehaviourlab.tracking.extract_flow_info import extract_flow_info, main


def test_extract_flow_info_adds_columns() -> None:
    df = pl.read_csv("tests/data/sample_vid_yolo_tracking_fixed_ids.csv")
    out = extract_flow_info(df)

    assert "dx" in out.columns
    assert "dy" in out.columns
    assert "speed" in out.columns
    assert "speed_smoothed" in out.columns
    assert out["speed"].dtype == pl.Float64
    assert len(out) == len(df)
    assert out["speed"].max() > 0


def test_extract_flow_info_empty_exits() -> None:
    df = pl.DataFrame(
        {
            "stable_id": pl.Series([], dtype=pl.Int64),
            "frame_id": pl.Series([], dtype=pl.Int64),
            "x": pl.Series([], dtype=pl.Float64),
            "y": pl.Series([], dtype=pl.Float64),
        }
    )
    with pytest.raises(SystemExit):
        extract_flow_info(df)


def test_main_writes_output(tmp_path: Path) -> None:
    input_csv = Path("tests/data/sample_vid_yolo_tracking_fixed_ids.csv")
    output_csv = tmp_path / "flow.csv"

    result = main.callback(input_csv, output_csv, False, False)
    assert result is None
    assert output_csv.exists()
    df_out = pl.read_csv(output_csv)
    assert "speed_smoothed" in df_out.columns
    assert df_out["speed"].max() > 0


def test_main_dry_run_does_not_write(tmp_path: Path) -> None:
    input_csv = Path("tests/data/sample_vid_yolo_tracking_fixed_ids.csv")
    output_csv = tmp_path / "flow.csv"

    result = main.callback(input_csv, output_csv, True, False)
    assert result is None
    assert not output_csv.exists()
