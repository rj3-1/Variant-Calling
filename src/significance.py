from scipy import stats
import pandas as pd

def test_significance(df):
    properties = [
        "protein_length",
        "molecular_weight",
        "isoelectric_point",
        "aromaticity",
        "instability_index",
        "gravy",
        "alpha_structure_fraction",
        "turn_structure_fraction",
        "beta_structure_fraction",
    ]

    disease_df = df[df["group"] == "disease"]
    control_df = df[df["group"] == "control"]

    results = {}
    for prop in properties:
        t_stat, p_value = stats.ttest_ind(
            disease_df[prop], control_df[prop], equal_var=False
        )
        results[prop] = {
            "disease_mean": disease_df[prop].mean(),
            "control_mean": control_df[prop].mean(),
            "t_statistic": t_stat,
            "p_value": p_value,
            "significant": p_value < 0.05,
        }

    significance_stats = pd.DataFrame.from_dict(results, orient="index")
    significance_stats.index.name = "property"

    return significance_stats