from django.shortcuts import render
from .models import Profile

# Create your views here.
def profiles(request):
    # group profiles by contribution_year
    profiles = Profile.objects.all()

    CURRENT_YEAR = '2022-2023'
    
    profiles_by_year = {}
    faculty_advisors = []

    # put students in profiles_by_year
    for profile in profiles:
        if profile.contribution_year == 'N/A' or profile.contribution_year == None:
            faculty_advisors.append(profile)

        else:
            if profile.contribution_year not in profiles_by_year:
                profiles_by_year[profile.contribution_year] = []
            profiles_by_year[profile.contribution_year].append(profile)

    context = {
        'profiles_by_year': profiles_by_year,
        'profiles': profiles,
        'CURRENT_YEAR': CURRENT_YEAR,
    }

    return render(request, 'users/profiles.html', context)
