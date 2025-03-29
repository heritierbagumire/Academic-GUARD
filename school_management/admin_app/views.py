from django.shortcuts import render
from .models import EnrollmentData
import pandas as pd
from sklearn.linear_model import LinearRegression
import json
from sklearn.metrics import r2_score

def admin_dashboard(request):
    # Fetch historical data
    enrollment_data = EnrollmentData.objects.all().order_by('year')
    
    # Default stats (latest year)
    latest_data = enrollment_data.last()
    total_students = latest_data.total_students if latest_data else 1248
    new_students = latest_data.new_students if latest_data else 356
    graduating_students = latest_data.graduating_students if latest_data else 274
    retention_rate = latest_data.retention_rate if latest_data else 86.0
    returning_students = total_students - new_students  # Returning students (excluding new)

    # Data for charts
    historical_years = [data.year for data in enrollment_data]
    historical_students = [data.total_students for data in enrollment_data]
    historical_new_students = [data.new_students for data in enrollment_data]
    historical_graduating_students = [data.graduating_students for data in enrollment_data]
    retention_rates = [data.retention_rate for data in enrollment_data]

    # Pie chart data for each year
    pie_chart_data_by_year = {}
    for data in enrollment_data:
        year = data.year
        pie_chart_data_by_year[year] = {
            'labels': ['Current Students', 'New Students', 'Graduating Students'],
            'values': [
                data.total_students - data.new_students - data.graduating_students,
                data.new_students,
                data.graduating_students
            ]
        }

    # Bar chart data (new and graduating students per year)
    # Instead of separate lists, create a list of dictionaries for easier iteration in the template
    bar_chart_data_list = [
        {
            'year': year,
            'new_students': new,
            'graduating_students': grad
        }
        for year, new, grad in zip(historical_years, historical_new_students, historical_graduating_students)
    ]
    # For the chart, we still need the separate lists
    bar_chart_data = {
        'years': historical_years,
        'new_students': historical_new_students,
        'graduating_students': historical_graduating_students
    }

    # Linear regression for historical trend (with R² score)
    r2 = 0  # Default R² score if no data
    if historical_years and historical_students:
        df = pd.DataFrame({
            'year': historical_years,
            'total_students': historical_students
        })
        X = df[['year']]
        y = df['total_students']
        model = LinearRegression()
        model.fit(X, y)
        r2 = r2_score(y, model.predict(X))

    # Default prediction parameters
    current_student_count = total_students
    new_students_per_year = new_students
    retention_rate_percent = retention_rate
    graduation_rate = (graduating_students / total_students * 100) if total_students else 22.0
    expected_growth_rate = 3.0

    # Initialize detailed predictions with default values
    detailed_predictions = {
        'current': {
            'total_students': current_student_count,
            'new_students': new_students_per_year,
            'returning_students': returning_students,
            'graduating_students': graduating_students,
        },
        'year_1': {
            'total_students': current_student_count,
            'new_students': new_students_per_year,
            'returning_students': returning_students,
            'graduating_students': graduating_students,
        },
        'year_3': {
            'total_students': current_student_count,
            'new_students': new_students_per_year,
            'returning_students': returning_students,
            'graduating_students': graduating_students,
        },
        'year_5': {
            'total_students': current_student_count,
            'new_students': new_students_per_year,
            'returning_students': returning_students,
            'graduating_students': graduating_students,
        },
    }
    growth_rate_5_years = 0

    # Handle form submission for predictions
    predictions = None
    if request.method == 'POST':
        current_student_count = int(request.POST.get('current_student_count', current_student_count))
        new_students_per_year = int(request.POST.get('new_students_per_year', new_students_per_year))
        retention_rate_percent = float(request.POST.get('retention_rate', retention_rate_percent))
        graduation_rate = float(request.POST.get('graduation_rate', graduation_rate))
        expected_growth_rate = float(request.POST.get('expected_growth_rate', expected_growth_rate))

        # Update current values based on form input
        detailed_predictions['current']['total_students'] = current_student_count
        detailed_predictions['current']['new_students'] = new_students_per_year
        detailed_predictions['current']['returning_students'] = current_student_count - new_students_per_year
        detailed_predictions['current']['graduating_students'] = int(current_student_count * (graduation_rate / 100))

        # Predict for 1 to 5 years
        future_years = [2024, 2025, 2026, 2027, 2028]  # 1 to 5 years from 2023
        predicted_students = [current_student_count] * 5 if not historical_years else model.predict(pd.DataFrame({'year': future_years}))

        # Adjust predictions based on form parameters
        adjusted_predictions = []
        current_students = current_student_count
        current_new_students = new_students_per_year
        current_graduating = detailed_predictions['current']['graduating_students']
        for i, year in enumerate(future_years):
            retained_students = current_students * (retention_rate_percent / 100)
            graduating = current_students * (graduation_rate / 100)
            retained_students -= graduating
            current_students = retained_students + current_new_students
            current_students *= (1 + expected_growth_rate / 100)
            current_new_students = int(current_new_students * (1 + expected_growth_rate / 100))
            current_graduating = int(current_students * (graduation_rate / 100))
            adjusted_predictions.append(round(current_students))

            # Store detailed predictions for years 1, 3, and 5
            if i == 0:  # Year 1
                detailed_predictions['year_1'] = {
                    'total_students': adjusted_predictions[-1],
                    'new_students': current_new_students,
                    'returning_students': adjusted_predictions[-1] - current_new_students,
                    'graduating_students': current_graduating,
                }
            elif i == 2:  # Year 3
                detailed_predictions['year_3'] = {
                    'total_students': adjusted_predictions[-1],
                    'new_students': current_new_students,
                    'returning_students': adjusted_predictions[-1] - current_new_students,
                    'graduating_students': current_graduating,
                }
            elif i == 4:  # Year 5
                detailed_predictions['year_5'] = {
                    'total_students': adjusted_predictions[-1],
                    'new_students': current_new_students,
                    'returning_students': adjusted_predictions[-1] - current_new_students,
                    'graduating_students': current_graduating,
                }

        # Calculate growth rate over 5 years
        if current_student_count != 0:
            growth_rate_5_years = ((adjusted_predictions[-1] - current_student_count) / current_student_count) * 100
        else:
            growth_rate_5_years = 0

        # Calculate percentage changes for each category
        for period in ['year_1', 'year_3', 'year_5']:
            for category in ['total_students', 'new_students', 'returning_students', 'graduating_students']:
                current_value = detailed_predictions['current'][category]
                future_value = detailed_predictions[period][category]
                if current_value != 0:
                    change = ((future_value - current_value) / current_value) * 100
                    detailed_predictions[period][f'{category}_change'] = round(change, 1)
                else:
                    detailed_predictions[period][f'{category}_change'] = 0

        predictions = {
            'years': future_years,
            'values': adjusted_predictions
        }

    context = {
        'total_students': total_students,
        'new_students': new_students,
        'graduating_students': graduating_students,
        'retention_rate': retention_rate,
        'historical_years': json.dumps(historical_years if historical_years else [2023]),
        'historical_students': json.dumps(historical_students if historical_students else [total_students]),
        'historical_new_students': json.dumps(historical_new_students if historical_new_students else [new_students]),
        'historical_graduating_students': json.dumps(historical_graduating_students if historical_graduating_students else [graduating_students]),
        'retention_rates': json.dumps(retention_rates if retention_rates else [retention_rate]),
        'pie_chart_data_by_year': json.dumps(pie_chart_data_by_year if pie_chart_data_by_year else {2023: {'labels': ['Current Students', 'New Students', 'Graduating Students'], 'values': [returning_students, new_students, graduating_students]}}),
        'bar_chart_data': json.dumps(bar_chart_data if bar_chart_data else {'years': [2023], 'new_students': [new_students], 'graduating_students': [graduating_students]}),
        'bar_chart_data_list': bar_chart_data_list if bar_chart_data_list else [{'year': 2023, 'new_students': new_students, 'graduating_students': graduating_students}],
        'r2_score': round(r2, 2),
        'predictions': predictions,
        'detailed_predictions': detailed_predictions,
        'growth_rate_5_years': round(growth_rate_5_years, 1),
        'current_student_count': current_student_count,
        'new_students_per_year': new_students_per_year,
        'retention_rate_percent': retention_rate_percent,
        'graduation_rate': graduation_rate,
        'expected_growth_rate': expected_growth_rate,
    }
    return render(request, 'admin/dashboard.html', context)

def page_preview(request):
    context = {
        'title': 'Sample Page Preview',
        'content': 'This is a preview of a sample page content. Imagine this could be a student profile or transcript details!'
    }
    return render(request, 'admin/preview.html', context)