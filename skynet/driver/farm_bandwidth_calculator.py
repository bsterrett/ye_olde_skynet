"""
    Thoughts:

    Bandwidth is the total amount of resources developed by a farm
    from the time of an attack which empties the resources of the
    farm to the time of the next attack. Both attacks must be
    conducted by you or someone in your alliance (but there is no
    way to definitively know this).

    Note that cranny dip can adversely affect this measurement.
    Random production by the farm, suddenly becoming active, can
    affect this measurement as well.

    If the latest attack on a farm did not empty the resources, or
    the farm has never been attacked before, the bandwidth be treated
    as infinite for now. Ideally the bandwidth should be estimated in
    a different regime, but that's probably not worth the effort.
"""
