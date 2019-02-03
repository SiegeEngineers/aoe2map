def count_voters(rms_instance):
    voters = None
    all_instances = get_all_rms_instances(rms_instance)
    for instance in all_instances:
        queryset = instance.vote_set.all().values_list('user_id', flat=True)
        if voters:
            voters |= queryset
        else:
            voters = queryset
    return voters.distinct().count()


def has_self_voted(rms_instance, user_id):
    all_instances = get_all_rms_instances(rms_instance)
    for instance in all_instances:
        if instance.vote_set.filter(user_id=user_id).exists():
            return True
    return False


def get_successors(rms_instance, predecessors):
    if rms_instance.newer_version and rms_instance.newer_version not in predecessors:
        predecessors.add(rms_instance.newer_version)
        return get_successors(rms_instance, predecessors)
    else:
        return predecessors


def get_predecessors(rms_instance):
    if rms_instance.predecessors.count() > 0:
        predecessors = {rms_instance}
        for predecessor in rms_instance.predecessors.all():
            predecessors |= get_predecessors(predecessor)
        return predecessors
    else:
        a = set()
        a.add(rms_instance)
        return a


def get_all_rms_instances(rms_instance):
    return get_successors(rms_instance, {rms_instance}) | get_predecessors(rms_instance)


def get_latest_version(map_version, depth=100):
    if depth < 0:
        return map_version
    else:
        depth -= 1
        if map_version.newer_version is None:
            return map_version
        else:
            return get_latest_version(map_version.newer_version, depth)
