from pathlib import Path
import pandas as pd
from pipeline.analyze_skills import parse_skills, top_skills, plot_top_skills


DATA_PATH = Path(__file__).parent / "data" / "ds_job_posts.csv"
OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    df = pd.read_csv(DATA_PATH)

    df["skills"] = df["skills"].apply(parse_skills)

    top = top_skills(df, top_n=30)
    top.to_csv(OUTPUT_DIR / "skills_summary.csv", index=False)

    plot_top_skills(top, OUTPUT_DIR / "skills_top.png")

    print("✅ Saved:\n")
    print(" > outputs/skills_summary.csv\n")
    print(" > outputs/skills_top.png")


if __name__ == "__main__":
    main()
