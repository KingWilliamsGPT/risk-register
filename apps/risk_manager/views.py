from collections.abc import Sequence
from django.db import models
from django.views import generic as g
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from core.settings import DEFAULT_PAGINATION_COUNT
from apps.authentication.models import Department
from .models import Risk
from .forms import AddRiskForm, RiskFilterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Count


from apps.authentication.models import Department, User
from apps.authentication.forms import AddDepartmentForm



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
            res['labels'].append(f'{risk_type} ({risk_count})')

        return JsonResponse(res, safe=False)

class RiskRatingSummary(LoginRequiredMixin, g.View):
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


class DepartmentListView(LoginRequiredMixin, g.ListView):
    model = Department
    template_name = 'risk_manager/departments/list.html'
    context_object_name = 'departments'
    paginate_by = settings.DEFAULT_PAGINATION_COUNT  # Show 10 risks per page



class DepartmentAddView(LoginRequiredMixin, g.CreateView):
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


class DepartmentDetailView(LoginRequiredMixin, g.DetailView):
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


class DepartmentUpdateView(LoginRequiredMixin, g.UpdateView):
    model = Department
    template_name = "risk_manager/departments/update.html"

