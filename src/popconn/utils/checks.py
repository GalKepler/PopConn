def validate_two_group_comparison(data, group_col):
    groups = data[group_col].unique()
    if len(groups) != 2:
        raise ValueError(f"Expected exactly 2 groups in '{group_col}', found: {groups}")
    return groups
