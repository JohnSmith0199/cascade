import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import TargetCriteria, URLParameter, CampaignData, CampaignMap


def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


export_as_csv.short_description = 'Export Data'


@admin.register(TargetCriteria)
class TargetCriteriaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TargetCriteria._meta.get_fields()]


@admin.register(URLParameter)
class URLParametersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in URLParameter._meta.get_fields()]


@admin.register(CampaignData)
class CampaignDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CampaignData._meta.get_fields()]
    action = [export_as_csv]


@admin.register(CampaignMap)
class CampaignMapAdmin(admin.ModelAdmin):
    list_display = [field.name for field in CampaignMap._meta.get_fields()]
