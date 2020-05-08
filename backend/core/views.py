from apps.events.models import Season


def get_custom_queryset(request, db_object):
    if request.query_params.get('season') == "all":
        print("Getting all events")
        return db_object.objects.all()

    print("Getting ONLY CURRENT season data")
    return db_object.objects.filter(season=Season.objects.get(current=True))
