from apps.events.models import Season


def get_object_custom_queryset(request, db_object):
    if request.query_params.get('season') == "all":
        print("Getting all events")
        return db_object.objects.all()

    # print("Getting ONLY CURRENT season data")
    return db_object.objects.filter(season=Season.objects.get(current=True))


# TODO refactor
def get_season_by_query(request, seasons):
    query = request.query_params.get('season')
    if query:
        if query == "current":
            seasons = seasons.filter(current=True)
        else:
            seasons = seasons.filter(year=query)
    return seasons
