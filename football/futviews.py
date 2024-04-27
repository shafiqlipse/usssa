from django.shortcuts import render, redirect
from athletes.models import Team
from football.models import Fixture
from football.models import Season, Group
from accounts.models import Sport
from football.models import Competition


# # Create your views here.
# def Teams(request):
#     teams = Team.objects.filter(sport_id=1)
#     context = {"teams": teams}
#     return render(request, "football/teams.html", context)


def footballFixtures(request):
    fixtures = Fixture.objects.all().order_by("-date")

    # Group fixtures by competition and then by date

    context = {"fixtures": fixtures}
    return render(request, "football/fixtures.html", context)


def footballResults(request):
    # Assuming the sport name is "football"
    fixtures = Fixture.objects.filter(competition=1).exclude(status="pending")
    # print(fixtures)
    context = {"fixtures": fixtures}
    return render(request, "football/results.html", context)


from collections import defaultdict


def footballStandings(request):
    sports = Sport.objects.all()

    standings_data = []

    for sport in sports:
        competitions = Competition.objects.filter(sport=sport)

        for competition in competitions:
            competition_standings = []

            groups = Group.objects.filter(competition=competition)

            for group in groups:
                fixtures = Fixture.objects.filter(group=group)

                # Dictionary to store standings for each team
                standings = defaultdict(lambda: defaultdict(int))

                # Initialize standings for all teams
                teams = group.teams.all()
                for team in teams:
                    standings[team]  # Initialize default values

                # Calculate standings
                for fixture in fixtures:
                    if (
                        fixture.team1_score is not None
                        and fixture.team2_score is not None
                    ):
                        standings[fixture.team1]["played"] += 1
                        standings[fixture.team2]["played"] += 1

                        standings[fixture.team1]["gs"] += fixture.team1_score
                        standings[fixture.team2]["gs"] += fixture.team2_score

                        standings[fixture.team1]["gc"] += fixture.team2_score
                        standings[fixture.team2]["gc"] += fixture.team1_score

                        if fixture.team1_score > fixture.team2_score:
                            standings[fixture.team1]["points"] += 3
                            standings[fixture.team1]["won"] += 1
                            standings[fixture.team2]["lost"] += 1
                        elif fixture.team1_score < fixture.team2_score:
                            standings[fixture.team2]["points"] += 3
                            standings[fixture.team2]["won"] += 1
                            standings[fixture.team1]["lost"] += 1
                        else:
                            standings[fixture.team1]["points"] += 1
                            standings[fixture.team2]["points"] += 1
                            standings[fixture.team1]["drawn"] += 1
                            standings[fixture.team2]["drawn"] += 1

                # Update goal difference
                for team, data in standings.items():
                    data["gd"] = data["gs"] - data["gc"]

                # Sort standings by points, goal difference, and goals scored
                sorted_standings = sorted(
                    standings.items(),
                    key=lambda x: (x[1]["points"], x[1]["gd"], x[1]["gs"]),
                    reverse=True,
                )

                competition_standings.append(
                    {"group": group, "standings": sorted_standings}
                )

            standings_data.append(
                {
                    "sport": sport,
                    "competition": competition,
                    "standings": competition_standings,
                }
            )

    context = {"standings_data": standings_data}

    return render(request, "football/standings.html", context)


# def footballNews(request):
#     pass
