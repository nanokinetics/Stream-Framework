from feedly.activity import Activity
from feedly.storage.cassandra.maps import ActivityMap
from feedly.storage.utils.serializers.base import BaseActivitySerializer
from feedly.verbs import get_verb_by_id
import pickle


class ActivitySerializer(BaseActivitySerializer):

    def get_serialized_activity(self, activity):
        return ActivityMap(
            key=activity.serialization_id,
            actor=activity.actor_id,
            time=activity.time,
            verb=activity.verb.id,
            object=activity.object_id,
            target=activity.target_id,
            entity_id=activity.extra_context.get('entity_id'),
            extra_context=pickle.dumps(activity.extra_context)
        )

    def loads(self, serialized_activities):
        activities = []
        for serialised_activity in serialized_activities:
            activity_kwargs = serialised_activity.__dict__.copy()
            activity_kwargs.pop('key')
            activity_kwargs.pop('entity_id')
            activity_kwargs['verb'] = get_verb_by_id(activity_kwargs['verb'])
            activity_kwargs['extra_context'] = pickle.loads(
                activity_kwargs['extra_context'])
            activities.append(Activity(**activity_kwargs))
        return activities
