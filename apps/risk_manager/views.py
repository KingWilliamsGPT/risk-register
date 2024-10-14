from collections.abc import Sequence
from django.views import generic as g
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from core.settings import DEFAULT_PAGINATION_COUNT
from .models import Risk
from .forms import AddRiskForm, RiskFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Count



class Dashboard(LoginRequiredMixin, g.TemplateView):
    template_name = "risk_manager/home.html"


class AddRisk(LoginRequiredMixin, g.CreateView):
    template_name = "risk_manager/add_risk.html"
    form_class = AddRiskForm
    model = Risk
    success_url = reverse_lazy('risk_register:risk_list')

    def form_valid(self, form):
        reponse = super().form_valid(form)
        self.object = form.save()
        response = HttpResponseRedirect(self.get_success_url())
        
        return response

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)
    

class RiskListView(LoginRequiredMixin, g.ListView):
    model = Risk
    template_name = 'risk_manager/risk_list.html'
    context_object_name = 'risks'
    paginate_by = settings.DEFAULT_PAGINATION_COUNT  # Show 10 risks per page

    def get_queryset(self):
        super().get_queryset
        queryset = Risk.objects.all()
        self.filter_form = form = RiskFilterForm(self.request.GET)

        if form.is_valid():
            risk_type = form.cleaned_data.get('risk_type')
            probability = form.cleaned_data.get('probability')
            impact = form.cleaned_data.get('impact')
            is_closed = form.cleaned_data.get('is_closed')

            if risk_type:
                queryset = queryset.filter(risk_type=risk_type)
            if probability:
                queryset = queryset.filter(probability=probability)
            if impact:
                queryset = queryset.filter(impact=impact)
            if is_closed:
                queryset = queryset.filter(is_closed=is_closed == 'True')

        return queryset.order_by(*self.get_ordering()) 

    def get_ordering(self):
        form = self.filter_form  # should be defined by now
        return ('-id', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RiskFilterForm(self.request.GET)
        return context




class RiskStat(LoginRequiredMixin, g.TemplateView):
    template_name = "risk_manager/risk_statistics.html"

class RiskPinned(LoginRequiredMixin, g.TemplateView):
    template_name = "risk_manager/risk_pinned.html"

class RiskPieSummary(LoginRequiredMixin, g.View):
    def get(self, request, *args, **kwargs):
        risk_distribution = Risk.objects.values('risk_type').annotate(count=Count('id'))
        
        res = {   
            'series': [],
            'labels': [],
        }

        for risk in risk_distribution:
            risk_type, risk_count = risk['risk_type'], risk['count']
            res['series'].append(risk_count)
            res['labels'].append(risk_type)

        return JsonResponse(res, safe=False)