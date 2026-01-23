#!/usr/bin/env python3

import polars as pl
import numpy as np
from pathlib import Path
import click
import matplotlib as mpl
from typing import List

mpl.use("Agg")
import matplotlib.pyplot as plt


def global_analysis(df: pl.DataFrame, output_dir: Path, file_stem: str) -> None:
    """
    Performs global analysis on the DataFrame and saves the results.

    Args:
        df (pl.DataFrame): The DataFrame containing bounding box data with columns:
            - stable_id: Object identifier
            - speed: Movement speed data
            - dx, dy: Movement vectors (for direction analysis)
        output_dir (Path): Directory to save the analysis outputs.
        file_stem (str): Stem of the input file name for output file naming.

    Returns:
        None

    Note:
        Creates the following output files:
        - {file_stem}_glob_speed_stats.csv: Global speed statistics
        - {file_stem}_glob_speed_hist.png: Global speed histogram
        - {file_stem}_obj_speed_stats.csv: Per-object speed statistics
        - {file_stem}_per_obj_speed_hist.png: Per-object speed histograms
        - {file_stem}_glob_dir_hist.png: Global direction histogram
        - {file_stem}_per_obj_dir_hist.png: Per-object direction histograms
    """
    click.echo("\n--- Global Speed Summary ---")
    df = df.filter(pl.col("speed").is_not_null())
    global_speed_stats = df["speed"].describe()
    click.echo(global_speed_stats)
    global_speed_stats.write_csv(output_dir / f"{file_stem}_glob_speed_stats.csv")

    num_rows: int = len(df)
    weights: np.ndarray = np.ones(num_rows) / num_rows

    plt.hist(df["speed"], bins=50, weights=weights, alpha=0.7)
    plt.margins(x=0)
    plt.title("Global Speed Distribution (Normalised)")
    plt.xlabel("Speed")
    plt.ylabel("Fraction of Rows")
    outpath = output_dir / f"{file_stem}_glob_speed_hist.png"
    plt.savefig(outpath)
    plt.close()
    click.echo(f"Saved global speed histogram to {outpath}")

    click.echo("\n--- Object-Level Speed Summaries ---")
    obj_speed_stats = df.group_by("stable_id").agg(
        [
            pl.col("speed").min().alias("min"),
            pl.col("speed").quantile(0.25).alias("25%"),
            pl.col("speed").median().alias("50%"),
            pl.col("speed").quantile(0.75).alias("75%"),
            pl.col("speed").max().alias("max"),
            pl.col("speed").mean().alias("mean"),
            pl.col("speed").std().alias("std"),
            pl.col("speed").count().alias("count"),
        ]
    )
    click.echo(obj_speed_stats)
    obj_speed_stats.write_csv(output_dir / f"{file_stem}_obj_speed_stats.csv")

    plt.figure()
    ids: List[int] = df["stable_id"].unique().to_list()
    for stable_id in ids:
        group = df.filter(pl.col("stable_id") == stable_id)
        speeds = group["speed"].to_numpy()
        n = speeds.shape[0]
        weights_obj = np.ones(n) / num_rows
        plt.hist(
            speeds,
            bins=50,
            alpha=0.5,
            label=f"ID={stable_id}",
            weights=weights_obj,
        )
    plt.title("Speed Distributions by ID (Normalised)")
    plt.xlabel("Speed")
    plt.margins(x=0)
    plt.ylabel("Fraction of All Rows")
    plt.legend()
    outpath = output_dir / f"{file_stem}_per_obj_speed_hist.png"
    plt.savefig(outpath)
    plt.close()
    click.echo(f"Saved per object speed histogram to {outpath}")

    click.echo("\n--- Global Direction Summary ---")
    df = df.with_columns(
        [
            pl.arctan2(pl.col("dy"), pl.col("dx")).alias("direction_rad"),
        ]
    )
    df = df.with_columns(
        [
            ((pl.col("direction_rad") * (180 / np.pi) + 360) % 360).alias(
                "direction_deg"
            ),
        ]
    )

    direction_stats = df.select("direction_deg").describe()
    click.echo(direction_stats)

    plt.hist(df["direction_deg"], bins=36, alpha=0.7, weights=weights)
    plt.title("Global Direction Distribution (Normalised)")
    plt.xlabel("Direction (degrees)")
    plt.ylabel("Fraction of Rows")
    plt.margins(x=0)
    outpath = output_dir / f"{file_stem}_glob_dir_hist.png"
    plt.savefig(outpath)
    plt.close()
    click.echo(f"Saved global direction histogram to {outpath}")

    plt.figure()
    for stable_id in ids:
        group = df.filter(pl.col("stable_id") == stable_id)
        dirs = group["direction_deg"].to_numpy()
        n = dirs.shape[0]
        weights_obj = np.ones(n) / num_rows
        plt.hist(
            dirs,
            bins=36,
            alpha=0.5,
            label=f"ID={stable_id}",
            weights=weights_obj,
        )
    plt.title("Direction Distributions by ID (Normalised)")
    plt.xlabel("Direction (degrees)")
    plt.ylabel("Fraction of Rows")
    plt.margins(x=0)
    plt.legend()
    outpath = output_dir / f"{file_stem}_per_obj_dir_hist.png"
    plt.savefig(outpath)
    plt.close()
    click.echo(f"Saved per object direction histogram to {outpath}")


# CLI Interface
@click.command()
@click.argument("input_csv", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(path_type=Path),
    help="Output directory. Defaults to input file directory.",
)
def main(input_csv: Path, output_dir: Path) -> None:
    """Generate movement analysis from object tracking data."""

    df = pl.read_csv(input_csv)

    # Validate required columns
    required_cols = ["stable_id", "speed", "dx", "dy"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise click.ClickException(f"Missing columns: {missing}")

    # Set defaults
    if output_dir is None:
        output_dir = input_csv.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    file_stem = input_csv.stem

    # Run analysis
    df_clean = df.filter(pl.col("speed").is_not_null())
    if len(df_clean) == 0:
        raise click.ClickException("No valid speed data found")

    global_analysis(df_clean, output_dir, file_stem)


if __name__ == "__main__":
    main()
