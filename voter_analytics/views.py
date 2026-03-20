from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from django.db.models.query import QuerySet
from django.shortcuts import render
import plotly.graph_objects as go
import plotly.io as pio
from django.db.models import Count

# Create your views here.

class VoterListView(ListView):
    """
    ListView for 
    """
    template_name = "voter_analytics/voters.html"
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        """
        Returns a queryset of voters that matches the selected filter.
        """
        results = super().get_queryset()

        # Filter by party affiliation
        part_af = self.request.GET.get("part_af")
        if part_af:
            results = results.filter(part_af=part_af)

        # Filter by minimum birth year
        min_year = self.request.GET.get("min_date")
        if min_year:
            results = results.filter(dob__year__gte=min_year)

        # Filter by maximum birth year
        max_year = self.request.GET.get("max_date")
        if max_year:
            results = results.filter(dob__year__lte=max_year)

        # Filter by voter score
        voter_score = self.request.GET.get("voter_score")
        if voter_score:
            results = results.filter(voter_score=voter_score)

        # Filter by election participation
        if self.request.GET.get("v20state"):
            results = results.filter(v20state=True)

        if self.request.GET.get("v21town"):
            results = results.filter(v21town=True)

        if self.request.GET.get("v21primary"):
            results = results.filter(v21primary=True)

        if self.request.GET.get("v22general"):
            results = results.filter(v22general=True)

        if self.request.GET.get("v23town"):
            results = results.filter(v23town=True)

        return results.order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        """
        Returns context data.
        """
        context = super().get_context_data(**kwargs)

        # Choices for form filters
        context["party_choices"] = (
            Voter.objects.values_list("part_af", flat=True)
            .distinct()
            .order_by("part_af")
        )

        context["year_choices"] = sorted(
            set(
                Voter.objects.values_list("dob__year", flat=True)
            )
        )

        context["score_choices"] = (
            Voter.objects.values_list("voter_score", flat=True)
            .distinct()
            .order_by("voter_score")
        )

        # preserve filters in pagination links
        params = self.request.GET.copy()
        params.pop("page", None)
        context["current_query"] = params.urlencode()

        return context


class VoterDetailView(DetailView):
    """
    DetailView for single voter information
    """
    template_name = "voter_analytics/voter.html"
    model = Voter
    context_object_name = "voter"

class GraphListView(ListView):
    """
    List view that also generates graphs for filtered voters.
    """

    template_name = "voter_analytics/graphs.html"
    model = Voter
    context_object_name = "voters"

    def get_queryset(self):
        """
        Returns a queryset of voters that matches the selected filter.
        """
        results = super().get_queryset()

        # Filter by party affiliation
        part_af = self.request.GET.get("part_af")
        if part_af:
            results = results.filter(part_af=part_af)

        # Filter by minimum birth year
        min_year = self.request.GET.get("min_date")
        if min_year:
            results = results.filter(dob__year__gte=min_year)

        # Filter by maximum birth year
        max_year = self.request.GET.get("max_date")
        if max_year:
            results = results.filter(dob__year__lte=max_year)

        # Filter by voter score
        voter_score = self.request.GET.get("voter_score")
        if voter_score:
            results = results.filter(voter_score=voter_score)

        # Filter by election participation
        if self.request.GET.get("v20state"):
            results = results.filter(v20state=True)

        if self.request.GET.get("v21town"):
            results = results.filter(v21town=True)

        if self.request.GET.get("v21primary"):
            results = results.filter(v21primary=True)

        if self.request.GET.get("v22general"):
            results = results.filter(v22general=True)

        if self.request.GET.get("v23town"):
            results = results.filter(v23town=True)

        return results.order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        """
        Return context data including the Graphs.
        """
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()

        # Choices for graph filter form
        context["party_choices"] = (
            Voter.objects.values_list("part_af", flat=True)
            .distinct()
            .order_by("part_af")
        )

        context["year_choices"] = sorted(
            set(
                Voter.objects.exclude(dob__isnull=True)
                .values_list("dob__year", flat=True)
            )
        )

        context["score_choices"] = (
            Voter.objects.values_list("voter_score", flat=True)
            .distinct()
            .order_by("voter_score")
        )

        context["selected_party"] = self.request.GET.get("part_af", "")
        context["selected_min_date"] = self.request.GET.get("min_date", "")
        context["selected_max_date"] = self.request.GET.get("max_date", "")
        context["selected_score"] = self.request.GET.get("voter_score", "")

        context["v20state_checked"] = "v20state" in self.request.GET
        context["v21town_checked"] = "v21town" in self.request.GET
        context["v21primary_checked"] = "v21primary" in self.request.GET
        context["v22general_checked"] = "v22general" in self.request.GET
        context["v23town_checked"] = "v23town" in self.request.GET

        # Graph 1: distribution by birth year
        birth_data = (
            qs.values("dob__year")
            .annotate(total=Count("id"))
            .order_by("dob__year")
        )

        birth_years = [row["dob__year"] for row in birth_data]
        birth_counts = [row["total"] for row in birth_data]

        fig_birth = go.Figure(
            data=[
                go.Bar(
                    x=birth_years,
                    y=birth_counts
                )
            ]
        )
        fig_birth.update_layout(
            title="Distribution of Voters by Year of Birth",
            xaxis_title="Year of Birth",
            yaxis_title="Number of Voters"
        )

        # Graph 2: distribution by party affiliation
        party_data = (
            qs.values("part_af")
            .annotate(total=Count("id"))
            .order_by("part_af")
        )

        party_labels = []
        party_counts = []
        for row in party_data:
            raw_party = row["part_af"]
            display_party = raw_party.strip() if raw_party else "(blank)"
            party_labels.append(display_party)
            party_counts.append(row["total"])

        fig_party = go.Figure(
            data=[
                go.Pie(
                    labels=party_labels,
                    values=party_counts
                )
            ]
        )
        fig_party.update_layout(
            title="Distribution of Voters by Party Affiliation"
        )

        # Graph 3: participation in each election
        election_labels = [
            "2020 State",
            "2021 Town",
            "2021 Primary",
            "2022 General",
            "2023 Town",
        ]

        election_counts = [
            qs.filter(v20state=True).count(),
            qs.filter(v21town=True).count(),
            qs.filter(v21primary=True).count(),
            qs.filter(v22general=True).count(),
            qs.filter(v23town=True).count(),
        ]

        fig_elections = go.Figure(
            data=[
                go.Bar(
                    x=election_labels,
                    y=election_counts
                )
            ]
        )
        fig_elections.update_layout(
            title="Voter Participation by Election",
            xaxis_title="Election",
            yaxis_title="Number of Voters"
        )

        # Convert figures to HTML
        context["birth_year_graph"] = pio.to_html(
            fig_birth,
            full_html=False,
            include_plotlyjs="cdn"
        )
        context["party_graph"] = pio.to_html(
            fig_party,
            full_html=False,
            include_plotlyjs=False
        )
        context["election_graph"] = pio.to_html(
            fig_elections,
            full_html=False,
            include_plotlyjs=False
        )

        return context
