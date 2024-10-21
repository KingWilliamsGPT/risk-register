from collections.abc import Sequence
from django.db import models
from django.db.models import Count, Sum
from django.views import generic as g
from django.http.response import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from djmoney.money import Money
from django.db.models import F

from apps.authentication.models import Department, User
from apps.authentication.forms import AddDepartmentForm

from .models import Risk
from .forms import AddRiskForm, RiskFilterForm
from .mixins import SuperUserMixin

DEFAULT_PAGINATION_COUNT = settings.DEFAULT_PAGINATION_COUNT
DEFAULT_CURRENCY_SYMBOL = '₦'
MAX_SEVERE_RISKS = 10

from django.core.exceptions import PermissionDenied


def get_most_severe_risks(num):
    return Risk.objects.annotate(
            severity=F('probability') * F('impact')
        ).order_by('-severity')[:num]


class Dashboard(SuperUserMixin, LoginRequiredMixin, g.TemplateView):
    template_name = "risk_manager/home.html"

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        kwargs['severe_risks'] = get_most_severe_risks(MAX_SEVERE_RISKS)
        return super().get_context_data(**kwargs)

class AddRisk(SuperUserMixin, LoginRequiredMixin, g.CreateView):
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
        """If the form
         is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)
    

class RiskListView(SuperUserMixin, LoginRequiredMixin, g.ListView):
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


class RiskDeleteView(SuperUserMixin, LoginRequiredMixin, g.View):
    model = Risk
    success_url = reverse_lazy('risk_register:risk_list')  # Replace with your desired redirect URL
    super_admin_only = True
    
    def get(self, request, pk):
        # the issue here is if users accidently navigate using get request data might be loss, but I don't want or need
        j = self.model.objects.all().filter(id=pk).delete()
        return redirect(self.success_url)


class RiskDetailView(SuperUserMixin, LoginRequiredMixin, g.UpdateView):
    model = Risk
    template_name = "risk_manager/risk_update.html"
    form_class = AddRiskForm
    context_object_name = 'risk'

    def get_success_url(self):
        # Redirect to the detail view of the updated risk after successful form submission
        return reverse_lazy('risk_register:risk_update', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        context = super().get_context_data(**kwargs)        
        context['form'] = self.form_class(instance=self.object)
        return context


class RiskStat(SuperUserMixin, LoginRequiredMixin, g.TemplateView):
    template_name = "risk_manager/risk_statistics.html"


class RiskPinned(SuperUserMixin, LoginRequiredMixin, g.TemplateView):
    template_name = "risk_manager/risk_pinned.html"


class RiskPieSummary(SuperUserMixin, LoginRequiredMixin, g.View):
    def get(self, request, *args, **kwargs):
        risk_distribution = Risk.objects.values('risk_type').annotate(count=Count('id'))
        MAX_LEN_RISK_TYPE = 7
        
        res = {
            'series': [],
            'labels': [],
            'tooltips': []  # Include tooltips for full names
        }

        for risk in risk_distribution:
            risk_type, risk_count = risk['risk_type'], risk['count']
            short_risk_type = (risk_type[:MAX_LEN_RISK_TYPE] + '...') if len(risk_type) > MAX_LEN_RISK_TYPE else risk_type  # Truncate after MAX_LEN_RISK_TYPE chars
            
            res['series'].append(risk_count)
            res['labels'].append(f'{short_risk_type} ({risk_count})')
            res['tooltips'].append(risk_type)  # Full risk type name for tooltip

        return JsonResponse(res, safe=False)


class RiskSuperSummaryView(SuperUserMixin, LoginRequiredMixin, g.View):
    def get(self, request, *args, **kwargs):
        # Aggregate the data
        opened_risks = Risk.objects.filter(is_closed=False)
        opened_risks_count = opened_risks.count()
        closed_risks_count = Risk.objects.filter(is_closed=True).count()
        
        # Sum the budgets for opened risks
        total_budget = opened_risks.aggregate(total_budget=Sum('risk_budget'))['total_budget'] or 0
        
        # Get currency symbol from the MoneyField
        budget_for_opened_risks_str = f"{DEFAULT_CURRENCY_SYMBOL}{total_budget:,.2f}" if total_budget else "₦0.00"

        # Prepare the response data
        response_data = {
            "opened_risks": opened_risks_count,
            "closed_risks": closed_risks_count,
            "budget_for_opened_risks": budget_for_opened_risks_str,
        }

        return JsonResponse(response_data)


class RiskSeveritySummaryView(SuperUserMixin, LoginRequiredMixin, g.View):
    def get(self, request, *args, **kwargs):
        # Get the top 10 most severe risks based on the rating
        most_severe_risks = get_most_severe_risks(num=10)

        # Prepare the response data
        response_data = []
        for risk in most_severe_risks:
            response_data.append({
                "risk_id": risk.id,
                "risk_type": risk.risk_type,
                "risk_description": risk.risk_description,
                "probability": risk.probability,
                "impact": risk.impact,
                "rating": risk.rating(), 
                "budget": f"{DEFAULT_CURRENCY_SYMBOL}{risk.risk_budget.amount:,.2f}" if risk.risk_budget else "₦0.00",
                "date_opened": risk.date_opened.isoformat(),
            })

        return JsonResponse(response_data, safe=False)

class RiskRatingSummary(SuperUserMixin, LoginRequiredMixin, g.View):
    def get(self, request, *args, **kwargs):
        risk_distribution = Risk.objects.annotate(
            rating=models.F('probability') * models.F('impact')
        ).values('rating').annotate(count=Count('id')).order_by('rating')
        
        res = {   
            'series': [],
            'labels': [],
        }

        for risk in risk_distribution:
            rating, risk_count = risk['rating'], risk['count']
            rating_info = Risk.rating_info(rating)
            label = f"{rating_info['tag']} ({risk_count})"
            res['series'].append(risk_count)
            res['labels'].append(label)

        return JsonResponse(res, safe=False)


class DepartmentListView(SuperUserMixin, LoginRequiredMixin, g.ListView):
    model = Department
    template_name = 'risk_manager/departments/list.html'
    context_object_name = 'departments'
    paginate_by = settings.DEFAULT_PAGINATION_COUNT  # Show 10 risks per page


class DepartmentAddView(SuperUserMixin, LoginRequiredMixin, g.CreateView):
    # TODO:
    # - instead of redirecting to the department list view go to the detail page after creating a department
    template_name = "risk_manager/departments/add.html"
    form_class = AddDepartmentForm
    model = Department
    success_url = reverse_lazy('risk_register:dept_list')

    def form_valid(self, form):
        reponse = super().form_valid(form)
        self.object = form.save()
        self.form = form
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('risk_register:dept_read', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)


class DepartmentDetailView(SuperUserMixin, LoginRequiredMixin, g.DetailView):
    model = Department
    template_name = "risk_manager/departments/details.html"
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        # if "form" not in kwargs:
        #     kwargs["form"] = self.get_form()
        department = self.get_object()
        staffs = department.staffs.order_by('is_super_admin')
        kwargs['staffs'] = staffs
        return super().get_context_data(**kwargs)


class DepartmentUpdateView(SuperUserMixin, LoginRequiredMixin, g.UpdateView):
    model = Department
    template_name = "risk_manager/departments/update.html"


class Page403(LoginRequiredMixin, g.TemplateView):
    template_name = 'risk_manager/403.html'
