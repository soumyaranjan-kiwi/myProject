import os
from django.shortcuts import render, redirect
from .forms import UserFileForm
import pandas as pd
from .models import UserFile, Feature, FeatureValidation, User
from datetime import datetime


def showformdata(request):
    """
        Function to handle form data submission.

        Parameters:
        - request: HTTP request object

        Returns:
        - HTTP response object
    """
    downloads_folder = os.path.expanduser('~')
    excel_file_path = os.path.join(downloads_folder, 'Downloads', 'task.xlsx')

    if request.method == 'POST':
        fm = UserFileForm(request.POST, request.FILES)

        if fm.is_valid():
            email = fm.cleaned_data['email']
            fm.save()
            user = User.objects.filter(email__icontains=email).first()
            df = pd.read_excel(excel_file_path)
            data = []
            for index, row in df.iterrows():
                Epic = row['Epic'] if not pd.isnull(row['Epic']) else ''
                Feature_name = row['Feature'] if not pd.isnull(row['Feature']) else ''
                Validation = row['Validation'] if not pd.isnull(row['Validation']) else ''
                AlertError_Message_if_required = row['AlertError_Message_if_required'] if not pd.isnull(
                    row['AlertError_Message_if_required']) else ''
                Start_Date = row['Start_Date'] if not pd.isnull(row['Start_Date']) else ''
                if Start_Date:
                    try:
                        Start_Date = datetime.strptime(Start_Date, '%Y/%m/%d').strftime('%Y-%m-%d')
                    except ValueError:
                        print(f"Invalid date format: {Start_Date}. Skipping this row.")
                        continue
                else:
                    Start_Date = None

                data.append([Epic, Feature, Validation, AlertError_Message_if_required, Start_Date])
                print(data)
                status = row['Status']
                if pd.isna(status):
                    status = 1
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

            return redirect('htmltable')
        else:
            print('Form is not valid:', fm.errors)
    else:
        fm = UserFileForm()
    return render(request, 'enroll/userregistration.html', {'form': fm})


def process_form_and_render_table(request):
    """
        Function to process form data and render a table.

        Parameters:
        - request: HTTP request object

        Returns:
        - HTTP response object
    """
    if request.method == 'GET':
        user_files = UserFile.objects.all()
        data = []
        for user_file in user_files:
            data.append({
                'Epic': user_file.epic,
                'Feature': ', '.join(feature.name for feature in user_file.features.all()),
                'Validation': ', '.join(
                    validation.msg for feature in user_file.features.all() for validation in feature.validations.all()),
                'error_message': user_file.error_msg,
                'start_date': user_file.start_date,
                'Status': user_file.get_status_display(),
            })
        return render(request, 'enroll/table.html', {'data': data})
    else:
        form = UserFileForm()

    return render(request, 'enroll/userregistration.html', {'form': form})
