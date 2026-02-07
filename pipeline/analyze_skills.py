from collections import Counter
import ast
import pandas as pd


def parse_skills(value) -> list[str]:
    '''
    convert skills column values to a list of strings.
    '''
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []

    if isinstance(value, list):
        return [str(x).strip().lower() for x in value if str(x).strip()]

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        try:
            parsed = ast.literal_eval(text)
            # "['',]" -> ['',]
            if isinstance(parsed, list):
                return [str(x).strip().lower() for x in parsed if str(x).strip()]
        except (ValueError, SyntaxError):
            pass
        return [x.strip().lower() for x in text.split(",") if x.strip()]

    return []


def top_skills(df: pd.DataFrame, skills_col: str="skills", top_n: int=30) -> pd.DataFrame:
    all_skills: list[str] = []
    for items in df[skills_col]:
        all_skills.extend(items)
    counter = Counter(all_skills)
    return (
        pd.DataFrame(counter.items(), columns=["skill", "count"])
        .sort_values("count", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def plot_top_skills(df_top: pd.DataFrame, output_path) -> bool:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return False

    if df_top.empty:
        return False

    plt.figure(figsize=(8, 6))
    plt.barh(df_top["skill"][::-1], df_top["count"][::-1])
    plt.xlabel("Count")
    plt.title("Top Skills")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return True
