from django.db import models


class RequirementDocument(models.Model):
    document_id = models.IntegerField(db_column='DocumentID', primary_key=True)

    description1 = models.CharField(db_column='Description1', max_length=255, blank=True, null=True)
    description2 = models.CharField(db_column='Description2', max_length=255, blank=True, null=True)
    description3 = models.CharField(db_column='Description3', max_length=255, blank=True, null=True)
    description4 = models.CharField(db_column='Description4', max_length=255, blank=True, null=True)

    responsible_name = models.CharField(db_column='ResponsibleName', max_length=255, blank=True, null=True)

    revision_number = models.IntegerField(db_column='RevisionNumber', blank=True, null=True)
    originated_date = models.DateTimeField(db_column='OriginatedDate', blank=True, null=True)
    revision_date = models.DateTimeField(db_column='RevisionDate', blank=True, null=True)

    document_group_policy_id = models.IntegerField(
        db_column='DocumentGroupPolicyId',
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'RequirementDocument'

    def __str__(self):
        return f"{self.document_id} - {self.description1 or ''}"