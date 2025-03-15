def millions_billions(value):
    """
    Format the economic loss value to show in millions or billions.

    Parameters
    ----------
    value : float
        The economic loss value.

    Returns
    -------
    str
        The formatted economic loss value.
    """
    if value >= 1e9:
        return f"${value / 1e9:.2f}B"
    else:
        return f"${value / 1e6:.2f}M"