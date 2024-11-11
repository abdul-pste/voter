from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    party_affiliation = forms.ChoiceField(
        choices=[('', 'All')] + [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()],
        required=False,
    )
    min_birth_year = forms.ChoiceField(
        choices=[('', 'Any')] + [(year, year) for year in range(1900, 2025)],
        required=False,
    )
    max_birth_year = forms.ChoiceField(
        choices=[('', 'Any')] + [(year, year) for year in range(1900, 2025)],
        required=False,
    )
    voter_score = forms.ChoiceField(
        choices=[('', 'Any')] + [(str(i), str(i)) for i in range(6)],
        required=False,
    )
    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)
