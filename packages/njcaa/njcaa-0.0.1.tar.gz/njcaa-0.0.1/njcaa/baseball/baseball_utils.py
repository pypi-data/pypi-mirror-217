from datetime import datetime


def get_njcaa_baseball_season(season: int) -> str:
    """
    Returns the NJCAA baseball season for an inputted season.

    Parameters
    ----------
    `season` (int, mandatory):
        The NJCAA baseball season you want 
        a properly formatted NJCAA season string from.

    Returns
    ----------
    A Properly formatted NJCAA season string
    """
    now = datetime.now()

    if season < 2013:
        raise ValueError('`season` must be greater than 2013.')
    elif season > now.year:
        raise ValueError(f'`season` must be greater than {now.year}.')

    return f'{season}-{str(season + 1)[2:4]}'


# get_njcaa_baseball_season(2013)
