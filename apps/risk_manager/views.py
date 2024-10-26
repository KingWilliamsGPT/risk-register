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
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear

from apps.authentication.models import Department, User
from apps.authentication.forms import AddDepartmentForm

from .models import Risk
from .forms import AddRiskForm, RiskFilterForm
from .mixins import SuperUserMixin
from .utils import render_template

DEFAULT_PAGINATION_COUNT = settings.DEFAULT_PAGINATION_COUNT
DEFAULT_CURRENCY_SYMBOL = '₦'
MAX_SEVERE_RISKS = 10

from django.core.exceptions import PermissionDenied


def get_most_severe_risks(num):
    return Risk.objects.annotate(
            severity=F('probability') * F('impact')
        ).order_by('-severity')[:num]

def _make_aware(date):
    try:
        data = timezone.make_aware(
            date,
            timezone.get_current_timezone()
        )
    except Exception:
        data = date
    return data

def _from_iso(isodate):
    isodate = isodate[:-1] if isodate.upper().endswith('Z') else isodate
    return timezone.datetime.fromisoformat(isodate)

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
    

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import ListView
from .models import Risk
from .forms import RiskFilterForm

class RiskListView(SuperUserMixin, LoginRequiredMixin, ListView):
    model = Risk
    template_name = 'risk_manager/risk_list.html'
    template_name_part = 'risk_manager/risk_list_part.html'
    template_name_part2 = 'risk_manager/risk_list_pagination_part.html'
    context_object_name = 'risks'
    paginate_by = 1 #settings.DEFAULT_PAGINATION_COUNT

    def get_queryset(self):
        queryset = Risk.objects.all()
        self.filter_form = form = RiskFilterForm(self.request.GET)

        if form.is_valid():
            risk_type = form.cleaned_data.get('risk_type')
            probability = form.cleaned_data.get('probability')
            impact = form.cleaned_data.get('impact')
            is_closed = form.cleaned_data.get('is_closed')
            search_string = form.cleaned_data.get('search_string')

            if risk_type:
                queryset = queryset.filter(risk_type=risk_type)
            if probability:
                queryset = queryset.filter(probability=probability)
            if impact:
                queryset = queryset.filter(impact=impact)
            if is_closed:
                queryset = queryset.filter(is_closed=is_closed == 'True')
            if search_string:
                queryset = queryset.filter(
                    models.Q(risk_description__icontains=search_string) | 
                    models.Q(risk_type__icontains=search_string) | 
                    models.Q(risk_owner__name__icontains=search_string) |
                    models.Q(risk_owner__code__icontains=search_string) |
                    models.Q(risk_owner__description__icontains=search_string)
                )


        return queryset.order_by(*self.get_ordering())

    def get_ordering(self):
        return ('-id', )

    def get_paginated_data(self, queryset):
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Include complete pagination context for AJAX handling
        data = {
            'risks': list(page_obj.object_list.values()),  # Convert queryset to list of dicts
            'page': page_obj.number,
            'pages': paginator.num_pages,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1,
        }
        self.data = data
        return data

    def get(self, request, *args, **kwargs):
        if self.is_fetched_request(request):
            # if using fetched request just return the html in parts, I could return json but that will mean more rendering logic on the frontend.
            self.template_name = self.template_name_part
            risk_html = super().get(request, *args, **kwargs).render().content.decode()
            self.get_paginated_data(self.object_list)
            pagination_html = render_template(self.template_name_part2, self.data)
            return JsonResponse({
                'risk_html': risk_html,
                'pagination_html': pagination_html,
            }, safe=False)

        return super().get(request, *args, **kwargs)

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


class RiskProgressChartView(SuperUserMixin, LoginRequiredMixin, g.View):
    def get(self, request, *args, **kwargs):
        # Retrieve query parameters
        view = request.GET.get('view', 'daily')
        start_date = request.GET.get('startDate')
        end_date = request.GET.get('endDate')

        # Parse dates
        start_date = _from_iso(start_date) if start_date else timezone.now() - timedelta(days=14)
        end_date = _from_iso(end_date) if end_date else timezone.now()

        start_date, end_date = min(start_date, end_date), max(start_date, end_date)

        # Set date extraction logic based on view (daily or monthly)
        labels = []
        opened_risks_data = []
        closed_risks_data = []

        if view == 'daily':
            days_range = (end_date - start_date).days + 1
            labels = [(start_date + timedelta(days=i)).strftime('%d %b') for i in range(days_range)]
            opened_risks_data = [0] * days_range
            closed_risks_data = [0] * days_range

            # Get opened risks and closed risks grouped by day
            opened_risks = Risk.objects.filter(is_closed=False, date_opened__range=(start_date, end_date))\
                .annotate(day=ExtractDay('date_opened')).values('day').annotate(count=Count('id')).order_by('day')
            closed_risks = Risk.objects.filter(is_closed=True, date_closed__range=(start_date, end_date))\
                .annotate(day=ExtractDay('date_closed')).values('day').annotate(count=Count('id')).order_by('day')

            # Populate opened_risks_data and closed_risks_data
            for entry in opened_risks:
                day = entry['day']
                index = (_make_aware(timezone.datetime(start_date.year, start_date.month, day)) - _make_aware(start_date)).days
                if 0 <= index < days_range:
                    opened_risks_data[index] = entry['count']

            for entry in closed_risks:
                day = entry['day']
                index = (_make_aware(timezone.datetime(start_date.year, start_date.month, day)) - _make_aware(start_date)).days
                if 0 <= index < days_range:
                    closed_risks_data[index] = entry['count']

        elif view == 'monthly':
            months_range = ((end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1)
            labels = [(start_date + timedelta(days=i*30)).strftime('%b %Y') for i in range(months_range)]
            opened_risks_data = [0] * months_range
            closed_risks_data = [0] * months_range

            # Get opened risks and closed risks grouped by month and year
            opened_risks = Risk.objects.filter(is_closed=False, date_opened__range=(start_date, end_date))\
                .annotate(month=ExtractMonth('date_opened'), year=ExtractYear('date_opened'))\
                .values('year', 'month').annotate(count=Count('id')).order_by('year', 'month')
            closed_risks = Risk.objects.filter(is_closed=True, date_closed__range=(start_date, end_date))\
                .annotate(month=ExtractMonth('date_closed'), year=ExtractYear('date_closed'))\
                .values('year', 'month').annotate(count=Count('id')).order_by('year', 'month')

            # Populate opened_risks_data and closed_risks_data
            for entry in opened_risks:
                year = entry['year']
                month = entry['month']
                index = (year - start_date.year) * 12 + (month - start_date.month)
                if 0 <= index < months_range:
                    opened_risks_data[index] = entry['count']

            for entry in closed_risks:
                year = entry['year']
                month = entry['month']
                index = (year - start_date.year) * 12 + (month - start_date.month)
                if 0 <= index < months_range:
                    closed_risks_data[index] = entry['count']

        # Prepare the response data
        response_data = {
            'labels': labels,
            'opened_risks': opened_risks_data,
            'closed_risks': closed_risks_data,
        }

        return JsonResponse(response_data)


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
