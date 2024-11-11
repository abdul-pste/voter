from django.shortcuts import render


from collections import Counter

import plotly.express as px
import plotly.graph_objs as go

from django.views.generic import ListView, DetailView, TemplateView
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

        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        if min_birth_year:
            queryset = queryset.filter(date_of_birth__year__gte = int(min_birth_year))
        if max_birth_year:
            queryset = queryset.filter(date_of_birth__year__lte = int(max_birth_year))
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

class GraphView(TemplateView):
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. Histogram: Voters by Year of Birth
        birth_years = [voter.date_of_birth.year for voter in Voter.objects.all()]
        birth_hist = px.histogram(
            x=birth_years,
            nbins=20,
            title="Voter Distribution by Year of Birth"
        )
        birth_hist.update_layout(
            xaxis_title="Year of Birth",
            yaxis_title="Number of Voters",
            bargap=0.2,
            template="plotly_dark",
            font=dict(size=14),
            title_font=dict(size=18, family="Arial"),
            width=900,
            height=500,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        birth_hist.update_traces(marker_color="lightblue")
        context['birth_hist'] = birth_hist.to_html()

        # 2. Pie Chart: Voter Distribution by Party Affiliation
        party_affiliation = Voter.objects.values_list('party_affiliation', flat=True)
        party_counts = Counter(party_affiliation)
        pie_chart = px.pie(
            names=list(party_counts.keys()),
            values=list(party_counts.values()),
            title="Voter Distribution by Party Affiliation"
        )
        pie_chart.update_traces(textinfo="percent+label")
        pie_chart.update_layout(
            template="plotly_dark",
            title_font=dict(size=18, family="Arial"),
            width=600,
            height=500,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        context['party_pie_chart'] = pie_chart.to_html()

        # 3. Bar Chart: Voter Participation in Elections
        participation_data = {
            "2020 State Election": Voter.objects.filter(v20state=True).count(),
            "2021 Town Election": Voter.objects.filter(v21town=True).count(),
            "2021 Primary": Voter.objects.filter(v21primary=True).count(),
            "2022 General Election": Voter.objects.filter(v22general=True).count(),
            "2023 Town Election": Voter.objects.filter(v23town=True).count(),
        }

        participation_hist = go.Figure(
            data=[
                go.Bar(
                    x=list(participation_data.keys()),
                    y=list(participation_data.values()),
                    marker=dict(color="lightgreen"),
                    text=list(participation_data.values()),
                    textposition='auto'
                )
            ]
        )
        participation_hist.update_layout(
            title="Voter Participation in Past Elections",
            xaxis_title="Election",
            yaxis_title="Number of Voters",
            template="plotly_dark",
            font=dict(size=14),
            title_font=dict(size=18, family="Arial"),
            width=900,
            height=500,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        context['participation_hist'] = participation_hist.to_html()

        return context