from organizacion.models import Organizacion
from encuesta.models import Encuesta
from comedor.models  import Comedor

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required


def report(request):
    return render_to_response(
        "admin/report.html",
        {'organizacion_list' : Organizacion.objects.all()},
        RequestContext(request, {}),
    )
report = staff_member_required(report)