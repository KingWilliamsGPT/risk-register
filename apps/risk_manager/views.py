from django.views import generic as g
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Risk
from .forms import AddRiskForm
from django.contrib.auth.mixins import LoginRequiredMixin




class Dashboard(LoginRequiredMixin, g.TemplateView):
    template_name = "risk_manager/home.html"


class AddRisk(LoginRequiredMixin, g.CreateView):
    template_name = "risk_manager/add_risk.html"
    form_class = AddRiskForm
    model = Risk
    success_url = reverse_lazy('risk_register:home')

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """Insert the form into the context dict."""
        if "form" not in kwargs:
            kwargs["form"] = self.get_form()
        return super().get_context_data(**kwargs)