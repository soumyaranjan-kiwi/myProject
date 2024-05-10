import os

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import UserFileForm
import pandas as pd
from .models import UserFile, Feature, FeatureValidation, User
from django.http import JsonResponse
from datetime import datetime
# from django.contrib.auth.decorators import login_required
from django.utils.functional import SimpleLazyObject


def showformdata(request):
    downloads_folder = os.path.expanduser('~')  # Gets the user's home directory
    excel_file_path = os.path.join(downloads_folder, 'Downloads', 'task.xlsx')

    if request.method == 'POST':
        fm = UserFileForm(request.POST, request.FILES)

        if fm.is_valid():
            email = fm.cleaned_data['email']
            fm.save()
            user = User.objects.filter(email__icontains=email).first()
            # Read Excel file and save its content into the database
            df = pd.read_excel(excel_file_path)  # Read Excel file from the specified path
            data=[]
            for index, row in df.iterrows():
                # Extract data from each row
                Epic = row['Epic'] if not pd.isnull(row['Epic']) else ''
                Feature_name = row['Feature'] if not pd.isnull(row['Feature']) else ''
                Validation = row['Validation'] if not pd.isnull(row['Validation']) else ''
                AlertError_Message_if_required = row['AlertError_Message_if_required'] if not pd.isnull(
                    row['AlertError_Message_if_required']) else ''
                Start_Date = row['Start_Date'] if not pd.isnull(row['Start_Date']) else ''

                # Convert date string to the correct format (from "YYYY/MM/DD" to "YYYY-MM-DD")
                if Start_Date:
                    try:
                        Start_Date = datetime.strptime(Start_Date, '%Y/%m/%d').strftime('%Y-%m-%d')
                    except ValueError:
                        print(f"Invalid date format: {Start_Date}. Skipping this row.")
                        continue  # Skip this row if date format is invalid
                else:
                    Start_Date = None  # Set to None if Start_Date is an empty string

                data.append([Epic, Feature, Validation, AlertError_Message_if_required, Start_Date])
                print(data)
                status = row['Status']
                if pd.isna(status):
                    status = 1  # Default value for NaN
                # Save data into the database
                print(user)
                user_file = UserFile.objects.create(
                    user=user,
                    epic=Epic,
                    error_msg=AlertError_Message_if_required,
                    start_date=Start_Date,
                    status=status
                )
                feature = Feature.objects.create(
                    user_file=user_file,
                    name=Feature_name
                )
                FeatureValidation.objects.create(
                    feature=feature,
                    msg=Validation
                )

            return redirect('htmltable')  # Redirect to the 'htmltable/' URL
        else:
            print('Form is not valid:', fm.errors)
    else:
        fm = UserFileForm()  # Assign a default value if the request method is not POST
    return render(request, 'enroll/userregistration.html', {'form': fm})


def process_form_and_render_table(request):
    if request.method == 'GET':
        user_files = UserFile.objects.all()
        data = []
        for user_file in user_files:
            data.append({
                'Epic': user_file.epic,
                'Feature': ', '.join(feature.name for feature in user_file.features.all()),
                'Validation': ', '.join(validation.msg for feature in user_file.features.all() for validation in feature.validations.all()),
                'Error Message': user_file.error_msg,
                'Start Date': user_file.start_date,
                'Status': user_file.get_status_display(),
            })
        return render(request, 'enroll/table.html', {'data': data})
    else:
        form = UserFileForm()

    return render(request, 'enroll/userregistration.html', {'form': form})