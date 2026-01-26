import polars as pl

from beehaviourlab.tracking.fix_ids import filter_out_feeder, fix_ids


def test_filter_out_feeder_removes_class() -> None:
    df = pl.DataFrame(
        {
            "frame_id": [0, 0],
            "class_id": [1, 2],
            "x": [0.0, 1.0],
            "y": [0.0, 1.0],
        }
    )
    filtered = filter_out_feeder(df)
    assert filtered["class_id"].to_list() == [2]


def test_fix_ids_handles_empty_dataframe() -> None:
    df = pl.DataFrame(
        {
            "frame_id": pl.Series([], dtype=pl.Int64),
            "x": pl.Series([], dtype=pl.Float64),
            "y": pl.Series([], dtype=pl.Float64),
        }
    )
    result = fix_ids(df, num_objects=2)
    assert result.is_empty()
    assert "stable_id" in result.columns


def test_fix_ids_interpolates_missing_detection() -> None:
    df = pl.DataFrame(
        {
            "frame_id": [0, 0, 1],
            "class_id": [2, 2, 2],
            "x": [0.0, 10.0, 0.5],
            "y": [0.0, 10.0, 0.5],
        }
    )
    result = fix_ids(df, num_objects=2).sort(["frame_id", "stable_id"])

    assert len(result) == 4
    frame1 = result.filter(pl.col("frame_id") == 1)
    assert frame1["stable_id"].to_list() == [1, 2]

    sid2 = frame1.filter(pl.col("stable_id") == 2)
    assert sid2["x"].to_list() == [10.0]
    assert sid2["y"].to_list() == [10.0]


def test_fix_ids_with_sample_csv() -> None:
    df = pl.read_csv("tests/data/sample_vid_yolo_tracking_raw.csv")
    result = fix_ids(df, num_objects=5)

    assert "stable_id" in result.columns
    assert result["stable_id"].min() >= 1
    assert result["stable_id"].max() <= 5
    assert result["frame_id"].n_unique() == df["frame_id"].n_unique()
