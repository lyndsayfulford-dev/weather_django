import json
import requests
from django.shortcuts import render

import json
import requests
from django.shortcuts import render

def home(request):
    # 1. Capture user input or fall back to a default area code (e.g., nv013)
	if request.method == "POST":
		reportingAreaCode = request.POST.get('reportingAreaCode', 'nv013')
	else:
		reportingAreaCode = 'nv013'

	# Clean the input to remove any stray spaces
	reportingAreaCode = reportingAreaCode.strip()

	# 2. Safely build the URL string using the variable
	api_url = f"https://www.airnowapi.org/aq/observation/current/racode/?format=application/json&reportingAreaCode={reportingAreaCode}&API_KEY=C7D4DE7F-24B0-45EC-879C-D2E7F6920561"
	api_request = requests.get(api_url)

	category_description = ""
	category_color = "normal"

	try:
		api = json.loads(api_request.content)
        
		if isinstance(api, list) and len(api) > 0:
			# Note: AirNow returns a list of dictionaries, grab the first one
			category_name = api[0].get('aqiCategoryName', '')

			if category_name == "Good":
				category_description = "(0 - 50) Air quality is considered satisfactory, and air pollution poses little or no risk."
				category_color = "good"

			elif category_name == "Moderate":    
				category_description = "(51 - 100) Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution."
				category_color = "moderate"        

			elif category_name == "USG":    
				category_description = "(101 - 150) Although general public is not likely to be affected at this AQI range, people with lung disease, older adults and children are at a greater risk from exposure to ozone, whereas persons with heart and lung disease, older adults and children are at greater risk from the presence of particles in the air."
				category_color = "usg"

			elif category_name == "Unhealthy":    
				category_description = "(151 - 200) Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
				category_color = "unhealthy"

			elif category_name.lower() == "very unhealthy":
				category_description = "(201 - 300) Health alert: everyone may experience more serious health effects."
				category_color = "very-unhealthy"

			elif category_name == "Hazardous":
				category_description = "(301 - 500) Health warnings of emergency conditions. The entire population is more likely to be affected."
				category_color = "hazardous"
		else:
			api = "Error..."

	except Exception as e:
		api = "Error..."

	return render(request, 'home.html', {
		'api': api,
		'category_description': category_description, 
		'category_color': category_color,
		'reportingAreaCode': reportingAreaCode,
	})


def about(request):
	return render(request, 'about.html', {})


