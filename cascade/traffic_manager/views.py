import logging
import shapely.wkt
import json

from django.shortcuts import redirect
from django.conf import settings
from django.utils.crypto import get_random_string

from .models import URLParameter, TargetCriteria, CampaignData, ValidationToken, CampaignMap


logger = logging.getLogger(__name__)


def __get_trigger(request, ip_addr):
    logger.debug('Request is %s' % request)
    param_maps = URLParameter.objects.values('ip', 'mid', 'geo')
    mid_triggers = TargetCriteria.objects.filter(type=TargetCriteria.TargetType.MID).values_list('value', flat=True)
    ip_triggers = TargetCriteria.objects.filter(type=TargetCriteria.TargetType.IP).values_list('value', flat=True)
    geo_triggers = TargetCriteria.objects.filter(type=TargetCriteria.TargetType.GEO).values_list('value', flat=True)

    for param_map in param_maps:
        if len(mid_triggers) > 0:
            tmp_mid = request.get(param_map['mid'])
            if tmp_mid is not None and tmp_mid in mid_triggers:
                return True
        if len(ip_triggers) > 0:
            tmp_ip = request.get(param_map['ip'])
            if tmp_ip is None:
                tmp_ip = ip_addr
            if tmp_ip is not None and tmp_ip in ip_triggers:
                return True
        if len(geo_triggers) > 0:
            tmp_geo = request.get(param_map['geo'])
            if tmp_geo is not None:
                for geo in geo_triggers:
                    tmp_poly = shapely.wkt.loads(geo)
                    if tmp_poly.contains(tmp_geo):
                        return True
    return False


def redirect_target(request, params, url):
    token_id = get_random_string(16)
    r = ValidationToken(token=token_id)
    r.save()
    if params and len(request.META['QUERY_STRING']) > 0:
        return redirect(url + '?%s' % request.META['QUERY_STRING'] + '&token_id=%s' % token_id)
    else:
        return redirect(url + '?token_id=%s' % token_id)


def index(request, campaign_id=None):
    params = request.GET
    trigger_state = __get_trigger(params, request.META['REMOTE_ADDR'])

    if campaign_id is None:
        return redirect(request, settings.CAMPAIGN_A_PARAMS, settings.CAMPAIGN_A)

    try:
        campaign_url = CampaignMap.objects.get(inbound_url=campaign_id)
    except:
        return redirect(request, settings.CAMPAIGN_A_PARAMS, settings.CAMPAIGN_A)

    if trigger_state and campaign_id is not None:
        record = CampaignData()
        record.data = json.dumps(params)
        record.save()
        return redirect_target(request, settings.CAMPAIGN_B_PARAMS, campaign_url.outbound_url)
    else:
        return redirect_target(request, settings.CAMPAIGN_A_PARAMS, settings.CAMPAIGN_A)
