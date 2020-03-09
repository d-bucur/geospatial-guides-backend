def to_object(model, selected=None, excluded=None):
    if isinstance(model, list):
        return [to_object(e, selected, excluded) for e in model]

    d = dict()
    for col in model.__table__.columns:
        if (selected is None or col.name in selected) \
                and (excluded is None or col.name not in excluded):
            d[_format_col_name(col.name)] = getattr(model, col.name)

    return d

    # ref: fields = {c.name: getattr(model, c.name) for c in model.__table__.columns}


def _format_col_name(name):
    words = name.split('_')
    words = [words[0]] + [word.capitalize() for word in words[1:]]
    return ''.join(words)
