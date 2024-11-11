from django.shortcuts import render

# Create your views here.


from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm  # We’ll create this form later



class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get filter values from GET request
        party_affiliation = self.request.GET.get('party_affiliation')
        min_birth_year = self.request.GET.get('min_birth_year')
        max_birth_year = self.request.GET.get('max_birth_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state') == 'on'
        v21town = self.request.GET.get('v21town') == 'on'
        v21primary = self.request.GET.get('v21primary') == 'on'
        v22general = self.request.GET.get('v22general') == 'on'
        v23town = self.request.GET.get('v23town') == 'on'

        # Apply filters if values are provided
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_birth_year))
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_birth_year))
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        if v20state:
            queryset = queryset.filter(v20state=True)
        if v21town:
            queryset = queryset.filter(v21town=True)
        if v21primary:
            queryset = queryset.filter(v21primary=True)
        if v22general:
            queryset = queryset.filter(v22general=True)
        if v23town:
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context
