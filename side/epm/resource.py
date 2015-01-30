from import_export import resources
from epm.models import party


class partyResource(resources.ModelResource):
    class Meta:
        model = party
